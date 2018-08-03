from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5

from apps.course.models import Course, CourseOrder


from utils import restful
# Create your views here.

def order_key(request):
    uid = '49dc532695baa99e16e01bc0'
    token = 'e6110f92abcb11040ba153967847b7a6'
    price = request.POST.get('price')
    istype = request.POST.get('istype')
    orderid = request.POST.get('orderid')
    goodsname = request.POST.get('goodsname')
    orderuid = str(request.user.id)
    notify_url = request.build_absolute_uri(reverse('payinfo:notify_url'))
    return_url = request.build_absolute_uri(reverse('course:course_detail',kwargs={
        "course_id": 1
    }))
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode('utf-8')).hexdigest()
    return restful.result(data={'key': key})

@csrf_exempt
def notify_url(request):
    return restful.ok()
