from django import forms
from .models import Teacher, Category, Course
from ..xfzauth.forms import FormMixin


class TeacherForm(forms.Form, FormMixin):
    class Meta:
        model = Teacher
        fields = ('name')

        error_messages = {
            'name': {
                'required': "请输入名字"
            }
        }


class CourseForm(forms.ModelForm, FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()

    class Meta:
        model = Course
        exclude = ('category', 'teacher', 'pub_time')

        error_messages = {
            'title': {
                'required': "title不能为空"
            },
            'video_url': {
                'required': "video_url不能为空"
            },
            'cover_url': {
                'required': "cover_url不能为空"
            },
            'price': {
                'required': "price不能为空"
            },
            'duration': {
                'required': "duration不能为空"
            },
            'profile': {
                'required': "profile不能为空"
            },
            'category_id': {
                'required': "category不能为空"
            },
            'teacher_id': {
                'required': "category不能为空"
            },
        }