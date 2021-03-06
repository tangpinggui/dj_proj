from django.urls import path
from .import views
from django.shortcuts import reverse

# 设置app命名空间
app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('news_list/', views.news_list, name='news_list'),
    path('news_detail/<news_id>/', views.news_detail, name='news_detail'),
    path('add_news_comment/', views.add_comment, name='add_news_comment'),
    path('search_news/', views.search_news, name='search_news'),
]

# url反转，反查
# app命名空间+url命名
# redirect(reverse('news:index'))