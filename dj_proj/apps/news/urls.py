from django.urls import path
from .import views
from django.shortcuts import reverse

# 设置app命名空间
app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
]

# url反转，反查
# app命名空间+url命名
# redirect(reverse('news:index'))