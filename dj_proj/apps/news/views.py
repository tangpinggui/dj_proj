from django.shortcuts import render, redirect, HttpResponse
from django.shortcuts import reverse
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings

from .models import News, NewsCategory
from .news_serializer import NewsSerializers

from utils import restful


@require_GET
def index(request):
    newses = News.objects.select_related('category', 'author')[0:settings.ONE_PAGE_NEWS_COUNT]
    categories = NewsCategory.objects.all()
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
