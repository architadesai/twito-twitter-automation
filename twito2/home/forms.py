from django import forms
from .models import ApplicationData, ApplicationAccess

class RegisterApp(forms.ModelForm):

    class Meta:

        model =  ApplicationData

        fields = [
            "appname",

        ]


class AccessApp(forms.ModelForm):

    class Meta:

        model = ApplicationAccess

        fields = [
            "accesstoken",
            "accesssecret",
            "consumerkey",
            "consumersecret",
        ]