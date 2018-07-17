from django.shortcuts import redirect
from utils import restful


def xfz_auth_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return restful.params_error(message="请登陆")
            return redirect('/account/login')
    return wrapper