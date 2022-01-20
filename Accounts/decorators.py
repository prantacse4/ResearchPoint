from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render, redirect

def IsResearcher(view_func):
    def wrap(request, *args, **kwargs):
        if (request.user.is_researcher == True) | (request.user.is_superuser == True):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrap


def IsUser(view_func):
    def wrap(request, *args, **kwargs):
        if (request.user.is_user == True) | (request.user.is_superuser == True):
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return wrap

