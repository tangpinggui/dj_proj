from django import forms

from ..xfzauth.forms import FormMixin
from .models import Banners


class AddBannersForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Banners
        fields = ('image_url', 'priority', 'jump_link')

        error_messages = {
            'image_url': {
                'required': "请选择轮播图"
            },
            'priority': {
                'required': "选择优先级"
            },
            'jump_link': {
                'required': "皮啥"}
        }


class ChangeBannerForm(forms.ModelForm, FormMixin):
    banner_id = forms.IntegerField()

    class Meta:
        model = Banners
        fields = ('image_url', 'priority', 'jump_link', 'banner_id')
