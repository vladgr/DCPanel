
from django.http import HttpResponseForbidden


class AccessControlMiddleware:
    def process_request(self, request):
        if request.META['REMOTE_ADDR'] != '127.0.0.1':
            message = 'Access from remote host is not allowed.'
            return HttpResponseForbidden(message)
