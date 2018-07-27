# -*- coding: utf-8 -*-
from django.forms import Form
from django import forms
from apps.xfzauth.forms import FormMixin
from .models import News, Comment


class NewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()  # 在表中属于外键字段，不能直接包括在 fileds里面

    class Meta:
        model = News
        fields = ('title', 'desc', 'content', 'thumbnail')  # here
        error_messages = {
            'category': {
                'required': '必须传入分类id'
            }
        }


class CommentForm(forms.Form, FormMixin):
    news_id = forms.IntegerField()
    content = forms.CharField()


class EditCmsNewForm(NewsForm):
    pk = forms.IntegerField()
    class Meta:
        model = News
        fields = ('title', 'desc', 'content', 'thumbnail', 'pk')  # here
