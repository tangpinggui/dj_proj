import json
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # 错误提示信息
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from django.views import View
from django.forms.utils import ErrorDict

from .models import User
from .forms import LoginForm, RegisterForm
from utils.captcha import hycaptcha
from utils.aliyunsdk.aliyun import send_sms
from utils import restful


def LoginView(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')

    if request.method == "POST":
        forms = LoginForm(request.POST)
        if forms.is_valid():
            data = forms.cleaned_data
            telephone = data["telephone"]
            password = data["password"]
            remember = data.get("remember")  # 前端设置的value
            # 验证数据是否正确
            user = authenticate(request, username=telephone, password=password)
            if user:
                login(request, user)  # 验证成功,登录,会在session中记录用户id, logout删除id
                if remember:
                    request.session.set_expiry(None)  # 设置None会使用默认的过期时间14天
                else:
                    request.session.set_expiry(0)  # 会话结束时过期
                return redirect(reverse("news:index"))
            else:
                messages.info(request, "账户或密码错误")
                return redirect(reverse("xfzauth:login"))
        else:
            messages.info(request, "请输入11位手机号码和6-20位密码")
            return redirect(reverse("xfzauth:login"))


def RegisterView(request):
    if request.method == "GET":
        return render(request, "auth/register.html")
    if request.method == "POST":
        # ##ajax中验证数据合法，前端
        forms = RegisterForm(request.POST)
        if forms.is_valid() and forms.validate_data(request):
            clean_data = forms.cleaned_data
            telephone = clean_data.get("telephone")
            password = clean_data.get("password")
            username = clean_data.get("username")
            user = User.objects.create_user(telephone=telephone, username=username, password=password)
            login(request, user)
            validata_result = forms.validate_data(request)
            return restful.ok()  # restful have JsonResponse
        else:
            message = forms.get_first_message()  # get_first_message自定义提取第一条错误信息
            return restful.params_error(message=message)

        # ##form验证数据合法，后端
        # forms = RegisterForm(request.POST)
        # if forms.is_valid() and forms.validate_data(request):
        #     forms.validate_data(request)
        #     clean_data = forms.cleaned_data
        #
        #     telephone = clean_data.get("telephone")
        #     password = clean_data.get("password")
        #     username = clean_data.get("username")
        #     user = User.objects.create_user(telephone=telephone, username=username, password=password)
        #     login(request, user)
        #     return redirect(reverse("news:index"))
        #
        # errors = forms.errors
        # # print(type(errors))  # <class 'django.forms.utils.ErrorDict'> ErrorDict可导入,
        # errors_dict = errors.get_json_data()  # ErrorDict类型转化为字典{'data1': [{'message': 'xx error', 'code': 字段}],}
        # if errors_dict:
        #     first_error_key = [key for key in errors_dict][0]  # data1
        #     first_error_list = errors_dict[first_error_key]  # [{'message': 'xx error', 'code': 字段}]
        #     first_error_message = first_error_list[0]['message']
        #
        #     messages.info(request, first_error_message)
        #
        # return redirect(reverse("xfzauth:register"))


def login_out(request):
    logout(request)
    return redirect('/')


def img_catpcha(request):
    """
    ## 图形验证码接口函数
    调用catpcha生成方法生成随机验证码，将验证码写入字节流io.BytesTO，再读取出来。
    HttpResponse对象才能识别
    """
    text, image = hycaptcha.Captcha.gene_code()
    # 存入session, forms中取出判断
    request.session["img_captcha"] = text

    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    response = HttpResponse(content_type="image/png")
    response.write(out.read())
    response['Content-length'] = out.tell()
    return response


def sms_captcha(request):
    """
    ## 手机短信验证码接口函数
    """
    code = hycaptcha.Captcha.gene_text()
    print("短信验证码是", code)
    request.session["short_auth"] = code

    telephone = request.GET.get("telephone")
    # result = send_sms(telephone, code)  # 调用阿里云短信服务接口
    # print(result, '短信发送的结果')
    return HttpResponse("success")
