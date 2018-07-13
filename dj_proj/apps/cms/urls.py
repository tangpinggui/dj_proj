from django.urls import path
from . import views


app_name = "cms"

urlpatterns = [
    path("", views.index, name='index'),
    path("write/news/", views.WriteNewsView.as_view(), name='write_news'),
    path("save_news/", views.save_thumbnail, name='save_news'),
    path("news/category/", views.news_category, name='news_category'),
    path("add_news_category/", views.add_news_category, name='add_news_category'),
    path("edit_news_category/", views.edit_news_category, name='edit_news_category'),
    path("del_news_category/", views.del_news_category, name='del_news_category'),
    path("qntoken/", views.qntoken, name='qntoken'),
]