import os
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required  # 登录装饰器
from django.utils.decorators import method_decorator
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from urllib import parse
from qiniu import Auth

from django.conf import settings
from .models import Banners
from .forms import AddBannersForm, ChangeBannerForm
from ..news.models import NewsCategory, News
from ..news.forms import NewsForm, EditCmsNewForm
from ..xfzauth.xfz_auth_required import xfz_auth_required

from utils import restful


# Create your views here.
# staff_member_required(login_url) 用来验证is_staff是否为真，判断用户能否登入cms页面，
# login_url是不通过验证跳转, 前端通过login函数登录后的user.is_staff判断是否显示
@staff_member_required(login_url='/')
def index(request):
    return render(request, 'cms/index.html')


# method_decorator 使装饰器装饰在类上面（装饰器的类装饰器？）  login_required 登陆验证,失败跳转
# despatch 类里面有多个方法（get,post）.将这些方法都装饰在despatch中,(通过despatch方法确定出get or post 再由login_required装饰)。
@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class WriteNewsView(View):
    def get(self, request):
        categories = NewsCategory.objects.all()
        return render(request, 'cms/write_news1.html', locals())

    def post(self, request):
        forms = NewsForm(request.POST)
        if forms.is_valid():
            cleaned_data = forms.cleaned_data
            title = cleaned_data.get('title')
            desc = cleaned_data.get('desc')
            thumbnail = cleaned_data.get('thumbnail')
            content = cleaned_data.get('content')
            author = request.user

            category_id = cleaned_data.get('category')
            category = NewsCategory.objects.get(id=category_id)
            try:
                News.objects.create(
                    title=title, desc=desc, thumbnail=thumbnail, content=content, category=category, author=author
                )
                return restful.ok()
            except:
                return restful.params_error("服务器gg")
        error = forms.get_first_message()
        return restful.params_error(error)

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)


@require_POST
def save_thumbnail(request):
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
        return restful.params_error(message='识别不了该文件')


@require_GET
def qntoken(request):
    access_key = 'qiniu access key'
    secret_key = 'qiniu secret key'
    bucket_name = 'qiniu space name'  # 七牛创建的储存空间名字

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name)
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


@xfz_auth_required
def banners(request):
    return render(request, 'cms/banners.html')


@require_POST
def add_banners(request):
    forms = AddBannersForm(request.POST)
    if forms.is_valid():
        try:
            image_url = forms.cleaned_data.get('image_url')
            priority = forms.cleaned_data.get('priority')
            jump_link = forms.cleaned_data.get('jump_link')
            banner = Banners.objects.create(image_url=image_url, priority=priority, jump_link=jump_link)
            banner_id = banner.pk
        except:
            return restful.params_error(message="服务器gg")
        return restful.result(data={'banner_id': banner_id}, message="轮播图添加成功")
    return restful.params_error(message=forms.get_first_message())


@require_POST
def banner_list(request):
    banners = list(Banners.objects.all().values())  # values将QuerySet对象里的数据转化成字典
    return restful.result(data={'banners': banners})


@require_POST
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banners.objects.get(id=banner_id).delete()
    return restful.result(message="轮播图删除成功")


@require_POST
def change_banner(request):
    forms = ChangeBannerForm(request.POST)
    if forms.is_valid():
        try:
            image_url = forms.cleaned_data.get('image_url')
            priority = forms.cleaned_data.get('priority')
            jump_link = forms.cleaned_data.get('jump_link')
            banner_id = forms.cleaned_data.get('banner_id')
            Banners.objects.filter(id=banner_id).update(image_url=image_url, priority=priority, jump_link=jump_link)
            return restful.result(data={"banner_id": banner_id, "csrf_token": csrf(request)}, message="轮播图修改成功")
        except:
            return restful.params_error(message="服务器出错")
    return restful.params_error(message="参数错误")


@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class NewsListView(View):
    def get(self, request):
        page = int(request.GET.get('page', 1))  # 第多少页,默认1
        newses = News.objects.select_related("category", "author").all()
        categories = NewsCategory.objects.all()
        ### 条件查询
        start_time = request.GET.get('start')
        end_time = request.GET.get('end')
        title = request.GET.get('title')
        category_id = int(request.GET.get('category', 0))

        if start_time and end_time:
            start_date = datetime.strptime(start_time, "%Y/%m/%d")
            end_date = datetime.strptime(end_time, "%Y/%m/%d")
            newses = newses.filter(pubtime__range=(start_date, end_date))
        if title:
            newses = newses.filter(title__icontains=title)
        if category_id:
            newses = newses.filter(category_id=category_id)

        ### 分页
        p = Paginator(newses, 5)  # 每页显示n条数据
        try:
            page_obj = p.page(page)  # 第n页的 page对象 <Page 1 of n>
        except:
            return redirect(reverse("cms:news_list"))
        current_page_newses = page_obj.object_list  # not func!! 当前页的newes所有数据 设置的是显示一条data
        context = {
            'newses': page_obj.object_list,
            'categories': categories,
            'p': p,
            'current_page': page,
            'start': start_time,
            'end': end_time,
            'title': title,
            'category_id': category_id,
            'url_parse': '&'+parse.urlencode({
                'start': start_time,
                'end': end_time,
                'title': title,
                'category': category_id
            })
        }
        context.update(self.get_paging_data(p, page_obj, show_pages=2, page=page))
        return render(request, 'cms/news_list.html', context=context)

    def post(self, request):
        return restful.ok()

    def get_paging_data(self, paginator, page_obj, show_pages, page=None):
        """
        分页当前页的左右范围
        :param paginator: Paginator(obj, number)对象
        :param page_obj: # 第n页的 page对象 <Page 1 of n> page_obj.number获取当前页
        :param show_pages: 当前页左右展示的页数
        :param page: 当前页  ps:可选参数
        :return: 当前页左右显示的页数range对象 和 has_left(right)_more Bool值，用来判断是否显示 分页的省略号 ...
        """
        current_page = page_obj.number
        show_pages = show_pages
        pages_number = paginator.num_pages

        has_left_more = False
        has_right_more = False
        # 左边的逻辑判断
        if current_page <= show_pages + 2:
            left_start = 1
            left_end = current_page
        else:
            has_left_more = True
            left_start = current_page - show_pages
            left_end = current_page
        left_range = range(left_start, left_end)
        # 右边的逻辑判断(在右边包括了当前页)
        if current_page >= pages_number - show_pages - 1:
            right_start = current_page
            right_end = pages_number + 1
        else:
            has_right_more = True
            right_start = current_page
            right_end = current_page + show_pages + 1
        right_range = range(right_start, right_end)
        data = {
            'left_range': left_range,
            'right_range': right_range,
            'has_left_more': has_left_more,
            'has_right_more': has_right_more,
            'current_page': current_page,
        }
        return data


@method_decorator(login_required(login_url='/account/login/'), name='dispatch')
class EditCmsNews(View):
    def get(self, request):
        edit_news_pk = request.GET.get('pk')
        news = News.objects.get(pk=edit_news_pk)
        categories = NewsCategory.objects.all()
        context = {
            'news': news,
            'pk': edit_news_pk,
            'categories': categories
        }
        return render(request, 'cms/write_news1.html', context=context)
    def post(self, request):
        forms = EditCmsNewForm(request.POST)
        if forms.is_valid():
            cleaned_data = forms.cleaned_data
            title = cleaned_data.get('title')
            desc = cleaned_data.get('desc')
            thumbnail = cleaned_data.get('thumbnail')
            content = cleaned_data.get('content')
            category = cleaned_data.get("category")
            pk = int(cleaned_data.get('pk'))
            pubtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            News.objects.filter(pk=pk).update(
                title=title,
                desc=desc,
                thumbnail=thumbnail,
                content=content,
                category=category,
                pubtime=pubtime
            )
            return restful.ok()
        return restful.params_error(message=forms.get_first_message())


@require_POST
def del_news(request):
    news_id = request.POST.get('pk')
    news = News.objects.filter(pk=news_id)
    print(news_id, news)
    if news:
        news.delete()
        return restful.ok()
    return restful.params_error(message="不存在的新闻")