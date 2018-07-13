from django.db import models
from apps.xfzauth.models import User


# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=100)


class News(models.Model):
    title = models.CharField(max_length=35)
    desc = models.CharField(max_length=100)
    thumbnail = models.URLField()
    content = models.TextField()
    pubtime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-pubtime']  # 以后进行News.object提取数据时，按照指定字段的排序提取数据
