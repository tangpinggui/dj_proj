from django.urls import path
from . import views
from apps.cms import staff_views


app_name = "cms"

urlpatterns = [
    path("", views.index, name='index'),
    path("write/news/", views.WriteNewsView.as_view(), name='write_news'),
    path("save_news/", views.save_thumbnail, name='save_news'),
    path("news_list/", views.NewsListView.as_view(), name='news_list'),
    path("news/category/", views.news_category, name='news_category'),
    path("add_news_category/", views.add_news_category, name='add_news_category'),
    path("edit_news_category/", views.edit_news_category, name='edit_news_category'),
    path("del_news_category/", views.del_news_category, name='del_news_category'),
    path("qntoken/", views.qntoken, name='qntoken'),
    path("banners/", views.banners, name='banners'),
    path("add_banners/", views.add_banners, name='add_banners'),
    path("banner_list/", views.banner_list, name='banner_list'),
    path("delete_banner/", views.delete_banner, name='delete_banner'),
    path("change_banner/", views.change_banner, name='change_banner'),
    path("edit_cms_news/", views.EditCmsNews.as_view(), name='edit_cms_news'),
    path("del_news/", views.del_news, name='del_news'),
    path("cms_course/", views.AddCourse.as_view(), name='cms_course'),
]

# 员工url配置
urlpatterns += [
    path('add_staff/', staff_views.AddStaff.as_view(), name='add_staff'),
    path('staff_list/', staff_views.staff_list, name='staff_list'),
    path('del_staff/', staff_views.del_staff, name='del_staff'),
]