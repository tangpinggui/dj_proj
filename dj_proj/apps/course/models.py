from django.db import models
from apps.xfzauth.models import User

class Category(models.Model):
    name = models.TextField()


class Teacher(models.Model):
    name = models.TextField()
    position = models.TextField()
    profile = models.TextField()
    avatar = models.URLField()


class Course(models.Model):
    title = models.TextField(max_length=100)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()  # 持续时间 秒
    profile = models.TextField()  # 课程简介
    pub_time = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, related_name="course", on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(Teacher, related_name="course", on_delete=models.DO_NOTHING)


class CourseOrder(models.Model):
    amount = models.FloatField()
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='order')
    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    statuse = models.SmallIntegerField()  # 1:代表未支付， 2：代表支付成功
    istype = models.SmallIntegerField(default=0)  # 1:支付宝支付， 2：代表微信支付, 0:代表未知
    pub_time = models.DateTimeField(auto_now_add=True)