from datetime import datetime, timedelta
import logging
from logging import Filter, getLoggerClass, setLoggerClass
from logging.handlers import TimedRotatingFileHandler
import os
import threading
import time
import traceback

# Thread-local storage for request ID
thread_local = threading.local()

class RequestIdFilter(Filter):
    def filter(self, record):
        record.request_id = getattr(thread_local, 'request_id', 'no_request_id')
        return True

class RequestIdLogger(getLoggerClass()):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        rv = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        rv.request_id = getattr(thread_local, 'request_id', 'no_request_id')

        # Include exec_info if available
        if hasattr(thread_local, 'exec_info'):
            rv.exec_info = thread_local.exec_info
        else:
            rv.exec_info = None

        return rv

    def exception(self, msg, *args, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        thread_local.exec_info = traceback.format_exc()
        super().exception(msg, *args, **kwargs)
        thread_local.exec_info = None  # Clear exec_info after logging

# Set the custom logger as the default logger class
setLoggerClass(RequestIdLogger)

class SizeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, max_bytes, keep_days, encoding=None):
        super().__init__(filename, when='midnight', interval=1, encoding=encoding)
        self.maxBytes = max_bytes
        self.suffix = "%Y%m%d_%H%M%S"
        self.keep_days = keep_days
        self.logger = logging.getLogger(__name__)

    def shouldRollover(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        return 0

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]

        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, time.gmtime()))
        if os.path.exists(dfn):
            count = 1
            dfn_base = dfn
            while os.path.exists(dfn):
                dfn = f"{dfn_base}.{count}"
                count += 1

        if os.path.exists(self.baseFilename):
            try:
                os.rename(self.baseFilename, dfn)
            except OSError:
                os.remove(self.baseFilename)

        if not self.delay:
            self.stream = self._open()
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if not dst_now:
                    addend = -3600
                else:
                    addend = 3600
                new_rollover_at += addend
        self.rolloverAt = new_rollover_at

        # Clean up old log files
        self.delete_old_logs()

    def delete_old_logs(self):
        """Delete log files based on the keep days"""
        dir_name, base_name = os.path.split(self.baseFilename)
        file_names = os.listdir(dir_name)
        prefix = base_name + "."
        current_time = datetime.now()
        for file_name in file_names:
            if file_name.startswith(prefix):
                file_path = os.path.join(dir_name, file_name)
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                # if (current_time - file_time) > timedelta(days=self.keep_days):
                if (current_time - file_time) > timedelta(minutes=1):
                    try:
                        os.remove(file_path)
                        self.logger.info(f"Deleted old log file: {file_path}")
                    except Exception as e:
                        self.logger.info(f"Error deleting {file_path}: {e}")


def create_timed_rotating_log_handler(filename, max_bytes=5 * 1024 * 1024, keep_days=10, encoding='utf-8'):
    log_dir = os.path.dirname(filename)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = SizeTimedRotatingFileHandler(filename, max_bytes=max_bytes, keep_days=keep_days, encoding=encoding)

    # Perform initial cleanup
    handler.delete_old_logs()

    return handler

def set_request_id(request_id):
    thread_local.request_id = request_id

def clear_request_id():
    if hasattr(thread_local, 'request_id'):
        del thread_local.request_id

# Add this new function
def get_request_id():
    return getattr(thread_local, 'request_id', 'no_request_id')
