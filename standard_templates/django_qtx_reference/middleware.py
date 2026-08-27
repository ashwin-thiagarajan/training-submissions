import json
import logging
import uuid

from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

from custom_logging import clear_request_id, set_request_id

logger = logging.getLogger(__name__)


class RequestResponseLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_id = str(uuid.uuid4())
        set_request_id(request_id)
        logger.info(f"Request started: {request.method} {request.path}")
        request.start_time = now()
        if request.body:
            try:
                body = json.loads(request.body)
                logger.info(f"Request Body: {json.dumps(body)}")
            except json.JSONDecodeError:
                logger.info(f"Request Body: {request.body.decode('utf-8')}")

    def process_response(self, request, response):
        logger.info(f"Response Status: {response.status_code}")
        if hasattr(response, 'data'):
            duration = now() - request.start_time
            logger.info(f"Response Data: {json.dumps(response.data)}")
            logger.info(f"Response Time: {duration.total_seconds():.3f} seconds")
        clear_request_id()
        return response
