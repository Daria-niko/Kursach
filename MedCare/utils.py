from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if 'role' in request.session and request.session['role'] == role:
                return view_func(request, *args, **kwargs)
            return redirect('login')  # Перенаправить на страницу входа, если роль не совпадает
        return _wrapped_view
    return decorator
