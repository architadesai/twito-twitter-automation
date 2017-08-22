from django import forms
from .models import (
    TwitterApp,

)

#https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

languages = (

    ('',''),
    ('Chinese', 'Chinese'),
    ('English', 'English'),
    ('Gujarati', 'Gujarati'),
    ('Hindi', 'Hindi'),
    ('Japanese', 'Japanese'),
    ('Marathi', 'Marathi'),
    ('Russian','Russian'),
    ('Sanskrit','Sanskrit'),

)


class TwitterAppForm(forms.ModelForm):
    class Meta:
        model = TwitterApp
        fields = ('appName', 'consumerKey', 'consumerToken')


class SearchLocationForm(forms.Form):
    class Meta:

        keyword = forms.CharField(max_length=100, required=False)
        lang = forms.ChoiceField(choices=languages,label='',initial='',widget=forms.Select(), required=False)
        latitude = forms.FloatField(required=True)
        longitude = forms.FloatField(required=True)
        radius = forms.CharField(required=True)
        radiusUnit = forms.ChoiceField(choices =(('km','km'),('mi','mi')),label='',initial='',widget=forms.Select(),required=True)

        # model = LocationSearch
        # fields = ('latitude','longitude','radius','radiusUnit')

class SerachKeywordForm(forms.Form):

    class Meta:
        keyword = forms.CharField(max_length=100, required=True)
        lang = forms.ChoiceField(choices=languages, label='', initial='', widget=forms.Select(), required=False)

class SearchUserForm(forms.Form):

    class Meta:

        userName = forms.CharField(max_length=30, required=True)


class PerformTaskForm(forms.Form):

    class Meta:

        likeTweets = forms.BooleanField(required=False)
        followUsers = forms.BooleanField(required=False)
        retweetTweets = forms.BooleanField(required=False)

