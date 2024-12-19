from .models import UserActionLog

class UserActionLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            action = f"{request.method} {request.path}"
            ip_address = self.get_client_ip(request)
            UserActionLog.objects.create(
                user=request.user,
                action=action,
                ip_address=ip_address
            )
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
