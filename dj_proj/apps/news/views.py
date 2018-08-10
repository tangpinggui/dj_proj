from django.shortcuts import render, redirect, HttpResponse
from django.shortcuts import reverse
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.http import Http404
from django.db.models import Q

from .models import News, NewsCategory, Comment
from .news_serializer import NewsSerializers, CommentSerializers
from .forms import CommentForm
from apps.xfzauth.xfz_auth_required import xfz_auth_required

from utils import restful
from apps.cms.models import Banners


@require_GET
def index(request):
    newses = News.objects.select_related('category', 'author')[0:settings.ONE_PAGE_NEWS_COUNT]
    categories = NewsCategory.objects.all()
    banners = Banners.objects.all()
    return render(request, 'news/index.html', locals())


@require_GET
def news_list(request):
    page = int(request.GET.get('page', 1))  # 前端请求第几页
    category_id = int(request.GET.get('category_id', 0))
    print(category_id, 'categoryid', '??')

    start = settings.ONE_PAGE_NEWS_COUNT * (page - 1)
    end = settings.ONE_PAGE_NEWS_COUNT + start
    """
    这种方法返回的News表中的外键数据为id，并不是需要的实际数据
    newses = News.objects.all()[start:end].values()  # values将QuerySet对象里的类容转换成字典
    newses = list(newses)
    """
    # 通过pip install djangorestframework, 使用该模块提供的序列化，使用方法官网。类似forms验证
    # 在进行序列化后
    if category_id:
        newses = News.objects.filter(category=category_id)[start:end]  # 注意这儿不要改动QuerySet类型，比如别使用value
    else:
        newses = News.objects.all()[start:end]  # 注意这儿不要改动QuerySet类型，比如别使用value
    serializer = NewsSerializers(newses, many=True)  # many代表外键字段取多个字段
    newses = serializer.data  # 获取serializer的json数据
    return restful.result(data=newses)


@require_GET
def news_detail(request, news_id):
    try:
        news = News.objects.select_related('author', 'category').get(id=news_id)
        news_count = news.comments.count()
        return render(request, 'news/news_detail.html', locals())
    except News.DoesNotExist:
        raise Http404  # Http404会从templates下面返回404.html


@require_POST
@xfz_auth_required
def add_comment(request):
    forms = CommentForm(request.POST)
    if forms.is_valid():
        clean_data = forms.cleaned_data
        content = clean_data.get('content')
        news_id = clean_data.get('news_id')
        news = News.objects.get(id=news_id)
        author = request.user
        comment = Comment.objects.create(content=content, news=news, author=author)
        serialize = CommentSerializers(comment)
        return restful.result(data=serialize.data)
    return restful.params_error(message=forms.get_first_message())

def search_news(request):
    tujian_news = News.objects.all()[:3]
    search_key = request.GET.get('q')
    if search_key:
        newses = News.objects.filter(Q(title__icontains=search_key)|Q(desc__contains=search_key)|Q(content__contains=search_key))
        if newses:
            context = {'newses': newses}
        else:
            context = {'noMatchAny': "暂时没有找到您需要的文章"}
    else:
        context = {}
    context.update({'tujian_news': tujian_news})
    return render(request, 'news/search.html', context=context)