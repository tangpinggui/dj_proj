from django import forms
from django.contrib import messages  # 错误提示信息
from django.shortcuts import reverse, redirect

from .models import User
from utils import restful


class FormMixin(object):
    """ 获取form验证的错误信息 """
    def get_first_message(self):
        errors = self.errors
        # print(type(errors))  # <class 'django.forms.utils.ErrorDict'> ErrorDict可导入,
        errors_dict = errors.get_json_data()  # ErrorDict类型转化为字典{'data1': [{'message': 'xx error', 'code': 字段}],}
        if errors_dict:
            first_error_key = [key for key in errors_dict][0]  # data1
            first_error_list = errors_dict[first_error_key]  # [{'message': 'xx error', 'code': 字段}]
            first_error_message = first_error_list[0]['message']
            return first_error_message
        return None


class LoginForm(forms.Form):
    """ 验证表单 """
    telephone = forms.CharField(min_length=11, max_length=11, error_messages={
        "required": "请输出手机号码",
        "min_length": "手机号码必须为11位",
        "max_length": "手机号码必须为11位",
    })
    password = forms.CharField(min_length=6, max_length=20, error_messages={
        "required": "请输入密码",
        "min_length": "密码至少为6位",
        "max_length": "密码不能超过20位",
    })
    remember = forms.IntegerField(required=False)  # 可以为空


class RegisterForm(forms.Form, FormMixin):
    """ register form auth """
    telephone = forms.CharField(min_length=11, max_length=11, error_messages={
        "required": "请输出手机号码",
        "min_length": "手机号码必须为11位",
        "max_length": "手机号码必须为11位",
    })
    username = forms.CharField(min_length=3, max_length=6, error_messages={
        "required": "请输入用户名",
        "min_length": "至少长度为3位的用户名",
        "max_length": "用户名长度过长，不超过6位",
    })
    img_auth = forms.CharField(min_length=4, max_length=4, error_messages={
        "required": "请输入图形验证码",
        "min_length": "图形验证码的长度不符",
        "max_length": "图形验证码的长度不符",
    })
    password = forms.CharField(min_length=6, max_length=20, error_messages={
        "required": "请输入密码",
        "min_length": "密码至少为6位",
        "max_length": "密码不能超过20位",
    })
    password1 = forms.CharField(min_length=6, max_length=20, error_messages={
        "required": "请再次输入密码",
        "min_length": "密码至少为6位",
        "max_length": "密码不能超过20位",
    })
    short_auth = forms.CharField(min_length=4, max_length=4, error_messages={
        "required": "请输入短信验证码",
        "min_length": "短信验证码的长度不符",
        "max_length": "短信验证码的长度不符",
    })

    def validate_data(self, request):
        clean_data = self.cleaned_data

        telephone = clean_data.get("telephone")
        exsits = User.objects.filter(telephone=telephone).exists()
        if exsits:
            # messages.info(request, "该手机号码已经注册")
            # return False
            return self.add_error("telephone", "该手机号码已经注册")

        server_img_captcha = request.session.get('img_captcha')
        img_captcha = clean_data.get("img_auth")
        if server_img_captcha.lower() != img_captcha.lower():
            # messages.info(request, "图形验证码错误")
            # return False
            return self.add_error("img_auth", "图形验证码错误")

        password = clean_data.get("password")
        password1 = clean_data.get("password1")
        if password != password1:
            # messages.info(request, "输入的密码不一致")
            # return False
            return self.add_error("password1", "输入的密码不一致")

        server_short_auth = request.session.get("short_auth")
        short_auth = clean_data.get("short_auth")
        if server_short_auth != short_auth:
            # messages.info(request, "短信验证码不正确")
            # return False
            return self.add_error("short_auth", "短信验证码不正确")
        return True