from django import forms
from .models import (
    TwitterApp,

)

#https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

languages = (
    #('Arabic','Arabic'),
    #('Bengali', 'Bengali'),
    #('Bihari Languages', 'Bihari Languages'),
    ('',''),
    ('Chinese', 'Chinese'),
    ('English', 'English'),
    #('German', 'German'),
    ('Gujarati', 'Gujarati'),
    ('Hindi', 'Hindi'),
    ('Japanese', 'Japanese'),
    #('Malayalam', 'Malayalam'),
    ('Marathi', 'Marathi'),
    ('Russian','Russian'),
    ('Sanskrit','Sanskrit'),
    #('Tamil','Tamil'),
    #('Telugu','Telugu'),

)


class TwitterApp_Form(forms.ModelForm):
    class Meta:
        model = TwitterApp
        fields = ('AppName', 'ConsumerKey', 'ConsumerToken','access_token','access_key')


class SearchLocation_Form(forms.Form):
    class Meta:

        keyword = forms.CharField(max_length=100, required=False)
        lang = forms.ChoiceField(choices=languages,label='',initial='',widget=forms.Select(), required=False)
        latitude = forms.FloatField(required=True)
        longitude = forms.FloatField(required=True)
        radius = forms.CharField(required=True)
        radiusUnit = forms.ChoiceField(choices =(('km','km'),('mi','mi')),label='',initial='',widget=forms.Select(),required=True)

        # model = LocationSearch
        # fields = ('latitude','longitude','radius','radiusUnit')


