from django.shortcuts import render, reverse, redirect
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import time, hashlib, hmac, os
from django.conf import settings
from hashlib import md5

from .models import Course, CourseOrder
from .forms import CourseForm

from utils import restful
from apps.xfzauth.xfz_auth_required import xfz_auth_required


def course_index(request):
    courses = Course.objects.all()
    return render(request, 'course/course_index.html', locals())


@xfz_auth_required
def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    bought = CourseOrder.objects.filter(buyer=request.user, course=course_id, statuse=2).exists()
    return render(request, 'course/course_detail.html', locals())


def course_token(request):
    """ 百度点播的token """
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    order = CourseOrder.objects.filter(course=course, statuse=2).exists()
    if not order:
        return restful.params_error('购买了吗')
    video_url = request.GET.get('video_url')
    # 过期时间
    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    extension = os.path.splitext(video_url)[1]  # .m3u8
    # 'mda-igjsr8g7z7zqwnav.m3u8'.replace('.m3u8', '') = 'mda-igjsr8g7z7zqwnav'
    media_id = video_url.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    print('token:', token)
    # a5e28c640e8436d9d0b7800116d1d59fc358229e8e448c5bb43d88fcdb114f83_92166a15820c4d2eb7798a57ee8230d2_1533032256
    return restful.result(data={'token': token})


def course_order(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    orders = CourseOrder.objects.filter(buyer=request.user, course=course)  # 未支付
    notify_url = request.build_absolute_uri(reverse('course:notify_url'))
    return_url = request.build_absolute_uri(reverse('course:course_detail', kwargs={
        "course_id": course_id
    }))
    if orders:
        order = orders[0]
        if order.statuse == 2:
            return redirect(reverse('course:course_detail', kwargs={'course_id': course_id}))
    else:
        order = CourseOrder.objects.create(amount=course.price, buyer=request.user, course=course, statuse=1)
    return render(request, 'course/create_order.html', locals())


def order_key(request):
    ''' 生成key '''
    uid = '49dc532695baa99e16e01bc0'
    token = 'e6110f92abcb11040ba153967847b7a6'
    price = request.POST.get('price')
    istype = request.POST.get('istype')
    orderid = request.POST.get('orderid')
    goodsname = request.POST.get('goodsname')
    orderuid = str(request.user.id)
    notify_url = request.build_absolute_uri(reverse('course:notify_url'))
    return_url = request.POST.get('return_url')

    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        'utf-8')).hexdigest()
    print(uid, price, notify_url, return_url, orderid, orderuid, goodsname, key)
    return restful.result(data={'key': key})


@csrf_exempt
def notify_url(request):
    print(request.POST, '???????')
    try:
        order_id = request.POST.get('orderid')
        CourseOrder.objects.filter(id=order_id).update(statuse=2)
    except:
        pass
    return restful.ok()
