# -*- coding: utf-8 -*-
from django.urls import path
from . import views


app_name = "payinfo"


urlpatterns = [
    path("notify_url/", views.notify_url, name='notify_url'),
    path("order_key/", views.order_key, name='order_key'),
]