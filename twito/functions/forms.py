from django import forms
from .models import TwitterApp


class TwitterApp_Form(forms.ModelForm):
    class Meta:
        model = TwitterApp
        fields = ('AppName', 'ConsumerKey', 'ConsumerToken','access_token','access_key')
