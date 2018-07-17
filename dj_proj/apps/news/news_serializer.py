# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import News, NewsCategory, Comment
from apps.xfzauth.user_serializer import UserSerializer


class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id', 'name')


class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializer()

    class Meta:
        model = News
        # 这里的category和author是外键字段需要额外指定序列化字段
        fields = ('id', 'title', 'desc', 'thumbnail', 'pubtime', 'category', 'author')


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')