from django.urls import path
from . import views


app_name = "xfzauth"

urlpatterns = [
    path("login/", views.LoginView, name='login'),
    path("register/", views.RegisterView, name='register'),
    # 图形验证码，短信验证码接口
    path("register/img/captcha/", views.img_catpcha, name='captcha'),
    path("register/sms/captcha/", views.sms_captcha, name='sms_captcha'),

    path("logout/", views.login_out, name='logout'),
    path("cmsadmin/", views.login_out, name='cmsadmin'),
]