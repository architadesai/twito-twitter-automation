from django.shortcuts import (
    render,

)
from django.contrib.auth.decorators import login_required

from .forms import RegisterApp


def index(request):
    return render(request, 'home/index.html')


@login_required
def applicationlogin(request):

    form = RegisterApp(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.username = request.user
        instance.save()


    return render(request, 'home/appdata.html', {"form":form})
