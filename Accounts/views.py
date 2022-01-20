from django.shortcuts import render, redirect,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages


from .models import User
from .decorators import IsResearcher, IsUser
from .forms import MyUserCreationForm

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=User.objects.get(email=email), password=password)
        except:
            user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            if (request.user.is_superuser == True):
                HttpResponseRedirect('/admin')
            return redirect('home')
        else:
            messages.error(request, 'Username, Email or Password is wrong')

    context = {'page':page}
    return render(request, 'Accounts/login_register.html', context)

# @login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    myform = MyUserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        myform = MyUserCreationForm(request.POST)
        is_researcher = False
        is_user = False

        user_type = request.POST.get('user_type')
        if user_type == "1":
             is_user = True
        else:
            is_researcher = True
        if myform.is_valid():
            user = myform.save(commit=False)
            user.username = user.username.lower()
            user.is_researcher = is_researcher
            user.is_user = is_user
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context ={'page':page, 'myform':myform}
    return render(request, 'Accounts/login_register.html', context)




