from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

FAILED_SERVICE_CALL_ERROR = _("Failed to service call error")
SERVICE_CALL_CODE = "service_call_error"


class InvalidInputFormatError(APIException):
    def __init__(self, detail=_("Invalid input format")):
        self.default_code = "invalid_input_format_error"
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class NeshanServiceCallError(APIException):
    status_code = 417

    def __init__(self, detail=FAILED_SERVICE_CALL_ERROR):
        self.default_code = SERVICE_CALL_CODE
        super().__init__(detail, self.default_code)
        self.default_detail = detail
