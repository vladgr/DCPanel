from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable.'


class BadRequest(APIException):
    status_code = 400
    default_detail = 'Bad Request'


class AccessForbidden(APIException):
    status_code = 403
    default_detail = 'Access Forbidden'


class NotImplemented(APIException):
    status_code = 404
    default_detail = 'Not implemented'
