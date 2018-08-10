from django.shortcuts import redirect
from django.utils.decorators import wraps
from django.contrib.auth.models import ContentType, Permission
from django.http import Http404

from apps.news.models import News, NewsCategory, Comment
from apps.cms.models import Banners
from apps.course.models import Course, CourseOrder, Category

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


def xfz_permission_required(model):
    ''' 该model的所有权都具备才可以验证通过 '''
    def decorator(viewfunc):
        @wraps(viewfunc)
        def _wrapper(request, *args, **kwargs):
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            # has_perms：只能采用字符串的形式判断
            # 字符串的形式为：app_label.codename
            codenames = [content_type.app_label+'.'+permission.codename for permission in permissions]
            # print(codenames)  # ['course.add_course', 'course.change_course', 'course.delete_course']
            # result = 0
            # for codename in codenames:
            #     if request.user.has_perm(codename):
            #         result+=1
            # print(result)

            ##  it's has_perms!!! not has_perm!!!
            result = request.user.has_perms(codenames)
            if result:
                return viewfunc(request, *args, **kwargs)
            else:
                raise Http404
        return _wrapper
    return decorator


def xfz_superuser_required(viewfunc):
    @wraps(viewfunc)
    def wrapper(requset, *args, **kwargs):
        if requset.user.is_superuser:
            return viewfunc(requset, *args, **kwargs)
        else:
            raise Http404
    return wrapper


def xfz_manager_required(viewfunc):
    @wraps(viewfunc)
    def _wrapper(request, *args, **kwargs):
        manager_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banners),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Category),
            ContentType.objects.get_for_model(CourseOrder),
        ]
        permissions = Permission.objects.filter(content_type__in=manager_content_types)
        print('permissions:', permissions)
        codenames = []
        for content_types in manager_content_types:
            codenames += [content_types.app_label + '.' + permission.codename for permission in permissions]
        print('codenames:', codenames)
        result = request.user.has_perms(codenames)
        print('result:', result)
        if result:
            return viewfunc(request, *args, **kwargs)
        else:
            raise Http404
    return _wrapper
