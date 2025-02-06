from threading import local
from django.utils.deprecation import MiddlewareMixin

_thread_locals = local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _thread_locals.user = getattr(request, 'user', None)