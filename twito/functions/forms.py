from django import forms
from .models import (
    TwitterApp,

)


class TwitterApp_Form(forms.ModelForm):
    class Meta:
        model = TwitterApp
        fields = ('AppName', 'ConsumerKey', 'ConsumerToken','access_token','access_key')


class SearchLocation_Form(forms.Form):
    class Meta:
        latitude = forms.FloatField()
        longitude = forms.FloatField()
        radius = forms.CharField()
        radiusUnit = forms.ChoiceField(choices =(('km','km'),('mi','mi')),label='',initial='',widget=forms.Select(),required=True)
        # model = LocationSearch
        # fields = ('latitude','longitude','radius','radiusUnit')



