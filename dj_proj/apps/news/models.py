from django.db import models
from apps.xfzauth.models import User


# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    title = models.CharField(max_length=25)
    desc = models.CharField(max_length=100)
    thumb = models.CharField(max_length=100)
    content = models.TextField(max_length=2000)
    pubtime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)