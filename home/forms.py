from django import forms
from .models import ApplicationData

class RegisterApp(forms.ModelForm):

    class Meta:

        model =  ApplicationData

        fields = [
            "appname",
            "consumerkey",
            "consumertoken"
        ]