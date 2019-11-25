from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout


def signup(request):
    if request.user.if_authenticated:
        return redirect('movies:index')
    


def login(request):
    pass


def logout(request):
    pass




