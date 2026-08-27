import logging

from pydantic import BaseModel, StrictInt, ValidationError


class RequestData(BaseModel):
    """
    Define Request data elements and their data types
    """

    mcc: StrictInt

#
class ValidateRequest:
    """
    This class defines the functions for validating Input Json from Rest API
    """

    def __init__(self):
        """To initiate logger variable"""
        self.logger = logging.getLogger(__name__)
        extra = {
            "cls_name": self.__class__.__name__,
        }
        self.logger = logging.LoggerAdapter(self.logger, extra)

    def request_validation(self, request):
        """
        :param request:
        :return:
        """
        # Validating Input Request Json

        try:
            RequestData(**request)
            return "valid"

        except ValidationError as e:
            self.logger.error(str(e))
            return "not valid parameters"
