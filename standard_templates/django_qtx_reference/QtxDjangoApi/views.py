import json
import logging
import os
import sys
import time

from rest_framework.response import Response
from rest_framework.views import APIView

from .errorcode import ErrorCodes
from .InputRequestValidation import ValidateRequest
from .ResponseJson import ResponseJson
from .models import MerchantCodes

class MccCode(APIView):
    """
    This View takes two numbers as input and does addition of two numbers
    and provides the sum as output
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.errorObj = ErrorCodes()
        self.responseObj = ResponseJson()
        self.sName = "Addition Service"
        self.status = 0
        extra = {
            "cls_name": self.__class__.__name__,
        }
        self.logger = logging.LoggerAdapter(self.logger, extra)

    def post(self, request):
        start_time = time.time()
        request_data = request.data
        input_request_validation_obj = ValidateRequest()
        end_time = time.time()
        mcc_description_json = None
        try:
            message = input_request_validation_obj.request_validation(request_data)

            if message == "valid":
                self.logger.info("Input request is valid so it can be processed")
                self.logger.info(request_data)
                request_data = request.data
                mcc = request_data["mcc"]
            elif message == "internal error":
                self.status = self.errorObj.InternalError
                self.logger.info(
                    self.sName
                    + "failed to process the request"
                    + "because of "
                    + str(self.errorObj.return_error_message(str(self.status)))
                )
                status_msg = self.errorObj.FailureMsg
                response = self.responseObj.response_json_object(
                    self.sName + str(self.errorObj.return_error_message(str(self.status))),
                    "0",
                    self.status,
                    status_msg,
                    -1,
                )
                return Response(response)
            else:
                self.status = self.errorObj.BadRequest
                self.logger.info(
                    self.sName
                    + "failed to process the request"
                    + "because of "
                    + str(self.errorObj.return_error_message(self.status))
                )
                status_msg = self.errorObj.FailureMsg
                response = self.responseObj.response_json_object(
                    self.sName + str(self.errorObj.return_error_message(self.status)),
                    "0",
                    self.status,
                    status_msg,
                    -1,
                )
                return Response(response)
        except KeyError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.logger.error(str([exc_type, f_name, exc_tb.tb_lineno]))
            self.logger.error(str(e))
            self.status = self.errorObj.InternalError
            status_msg = self.errorObj.FailureMsg
            response = self.responseObj.response_json_object(
                self.sName + str(self.errorObj.return_error_message(self.status)),
                "0",
                self.status,
                status_msg,
                -1,
            )
            return Response(response)

        try:
            self.logger.debug("Processing started")
            start_time = time.time()
            mcc_description = (
                MerchantCodes.objects.filter(mcc_code=mcc)
            )

            records_list = list(mcc_description.values())

            # Convert to JSON string
            mcc_description_json = json.dumps(records_list)

            print(mcc_description_json)

            end_time = time.time()
            self.status = 200
        except Exception as e:
            self.logger.exception(e)
            self.status = 500

        if self.status == 200:
            status_msg = self.errorObj.SuccessMsg
        else:
            status_msg = self.errorObj.FailureMsg

        response = self.responseObj.response_json_object(
            self.sName + str(self.errorObj.return_error_message(self.status)),
            end_time - start_time,
            self.status,
            status_msg,
            mcc_description_json,
        )

        return Response(response)
