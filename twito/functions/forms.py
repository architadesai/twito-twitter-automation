from django import forms
from .models import TwitterApp


class TwitterApp_Form(forms.ModelForm):
    class Meta:
        model = TwitterApp
        fields = ('AppName', 'ConsumerKey', 'ConsumerToken',)


class csv_file(forms.Form):
    csv_file = forms.FileField()
