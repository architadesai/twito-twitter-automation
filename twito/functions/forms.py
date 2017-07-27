from django import forms
from .models import (
    TwitterApp,
    LocationSearch,
)


class TwitterApp_Form(forms.ModelForm):
    class Meta:
        model = TwitterApp
        fields = ('AppName', 'ConsumerKey', 'ConsumerToken','access_token','access_key')


class SearchLocation_Form(forms.ModelForm):
    class Meta:
        model = LocationSearch
        fields = ('latitude','longitude','radius','radiusUnit')



    # latitude = forms.FloatField()
    # longitude  = forms.FloatField()
    # radius = forms.CharField()