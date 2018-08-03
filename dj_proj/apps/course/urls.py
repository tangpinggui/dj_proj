from django.urls import path
from . import views


app_name = "course"


urlpatterns = [
    path("course_index/", views.course_index, name='course_index'),
    path("course_detail/<course_id>/", views.course_detail, name='course_detail'),
    path("course_token/", views.course_token, name='course_token'),
    path("course_order/", views.course_order, name='course_order'),
    path("order_key/", views.order_key, name='order_key'),
    path("order_key/", views.order_key, name='order_key'),
    path("notify_url/", views.notify_url, name='notify_url'),
]


