from rest_framework.exceptions import APIException


class IPStackConnectionError(APIException):
    status_code = 503
    default_detail = 'Service unavailable.'
    default_code = 'service_unavailable'
