from .models import UserActionLog

def log_user_action(user, action, ip_address=None, additional_info=None):
    UserActionLog.objects.create(
        user=user,
        action=action,
        ip_address=ip_address,
        additional_info=additional_info,
    )
