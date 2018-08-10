# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.http import Http404

from apps.xfzauth.models import User
from apps.xfzauth.xfz_auth_required import xfz_superuser_required, xfz_manager_required

from utils import restful


def staff_list(request):
    staffs = User.objects.filter(is_staff=True)
    return render(request, 'cms/staff_list.html', locals())


@method_decorator(xfz_superuser_required, name='dispatch')
class AddStaff(View):
    def get(self, request):
        groups = Group.objects.all()
        return render(request, 'cms/add_staff.html', locals())
    def post(self, request):
        staff_groups = request.POST.getlist('staff_group')
        staff_phone = request.POST.get('staff_phone')
        user = User.objects.filter(telephone=staff_phone)
        if not user:
            return HttpResponse('no this telephone! are you registered?')
        user[0].is_staff = True
        if staff_groups:
            user[0].groups.set(Group.objects.filter(pk__in=staff_groups))
        user[0].save()
        return redirect(reverse('cms:staff_list'))


@require_POST
@xfz_manager_required
def del_staff(request):
    telephone = request.POST.get('telephone')
    if telephone:
        user = User.objects.get(telephone=telephone)
        if user.is_superuser:
            return restful.params_error('超级管理员不能被删除')
        else:
            user.is_staff = False
            user.save()
            user.groups.clear()
            return restful.ok()
    else:
        return restful.params_error('未获取到手机号码')