import os
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from qiniu import Auth

from django.conf import settings
from ..news.models import NewsCategory

from utils import restful


# Create your views here.
# staff_member_required(login_url) 用来验证is_staff是否为真，判断用户能否登入cms页面，
# login_url是不通过验证跳转, 前端通过login函数登录后的user.is_staff判断是否显示
@staff_member_required(login_url='/')
def index(request):
    return render(request, 'cms/index.html')


class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        return render(request, 'cms/write_news1.html', locals())

    def post(self, request):
        """ 文件本地储存  """
        try:
            file_content = request.FILES.get('upfile')
            sysfile = os.path.abspath('.') + '/' + 'media'
            file_save_path = os.path.join(sysfile, file_content.name)
            with open(file_save_path, 'wb') as f:
                for chunk in file_content.chunks():
                    f.write(chunk)
            # build_absolute_uri 自动返回服务器的地址
            url = request.build_absolute_uri(settings.MEDIA_URL + file_content.name)
            return restful.result(data={'url': url})
        except:
            return restful.params_error('识别不了该文件')


@require_GET
def qntoken(request):
    access_key = 'qiniu access key'
    secret_key = 'qiniu secret key'
    bucket_name = 'qiniu space name'  # 七牛创建的储存空间名字

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
    print(token)
    return restful.result(data={'token': token})


def news_category(request):
    categories = NewsCategory.objects.order_by('-id')  # 倒序
    return render(request, 'cms/news_category1.html', locals())


@require_POST
def add_news_category(request):
    name = request.POST.get('name')
    exiets = NewsCategory.objects.filter(name=name).exists()
    if not exiets:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="分类已存在")


@require_POST
def edit_news_category(request):
    name = request.POST.get('name')
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(id=pk).update(name=name)
        return restful.ok()
    except:
        return restful.params_error(message='修改的分类，被怪兽吃掉了。嘤嘤嘤')


@require_POST
def del_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(id=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='该分类，已经被怪兽吃掉了。emmmm')
