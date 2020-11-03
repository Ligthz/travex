from django.shortcuts import render, redirect 
from django.http import HttpResponse, JsonResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils import timezone

# Create your views here.
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only, active_only

import random
import string
import colorsys
import json
import datetime

def randomString():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(12))

def time_now():
    current_time = datetime.datetime.now()#+datetime.timedelta(hours=16)
    #current_time = datetime.datetime(2020, 8, 24)
    
    
    return current_time    

# ======================== Login related =========================================

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('mobile-home')

        

    context = {'form':form}
    return render(request, 'mobile/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        #print(request.POST)
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mobile-home')
        else:
            try:
                user = Account.objects.get(username=username)
                return render(request, 'mobile/login.html', {'message':'Please wait for admin to activate your account.'})
            except Exception:
                return render(request, 'mobile/login.html', {'message':'Username OR password is incorrect.'})
            
    context = {}
    return render(request, 'mobile/login.html', context)

@login_required(login_url='mobile-login')
def logoutUser(request):
    logout(request)
    #record_action(request.user,"Logout")
    return redirect('mobile-login')

# ======================== Dashboard =========================================        
def record_action(user,action):
    #user = Account.objects.get(username=str(user))
    #action_obj = UserAction(user = user, action = action)
    #action_obj.save()
    pass


def get_events(time_range,**kwargs):
    data_objs = LogData.objects.filter(DateCreated__range=time_range,**kwargs)#,PIC=user.name)
    if len(data_objs) == 0:
        context = {'NoData':True,'data':{"para":[],"data":[]}}
    else:
        datas = {}
        datas["para"] = data_objs[0].parameter()
        datas["data"] = []
        for obj in data_objs:
            datas["data"].append(obj.list())
        context = {'NoData':False,'data':datas}
    return context


@login_required(login_url='mobile-login')
@active_only
def home(request):
    user = request.user
    transactions = UserTransaction.objects.filter(user=user)

    return render(request, 'mobile/dashboard.html',{'user': user,'transactions':transactions})


@login_required(login_url='mobile-login')
@active_only
def Portfolio(request):
    user = request.user
    portfolio_obj = Portfolio_data.objects.last()
    return render(request, 'mobile/portfolio.html',{'portfolio': portfolio_obj})


@login_required(login_url='mobile-login')
@active_only
def About_Traves(request):
    user = request.user
    about_obj = About_data.objects.last()

    return render(request, 'mobile/about.html',{'about': about_obj})


@login_required(login_url='mobile-login')
@active_only
def latest_news(request):
    user = request.user
    contents = Blog.objects.all()

    return render(request, 'mobile/latest_news.html',{'user': user,'contents':contents})


@login_required(login_url='mobile-login')
def userPage(request):
    output_text = "Please await for confirmation for this account after signup..."

    record_action(request.user,"Un-authenticated")
    context = {'output_text':output_text}
    return render(request, 'accounts/user.html', context)




# ======================== Account Setting =========================================

@login_required(login_url='login')
def accountSettings(request):
    user = request.user
    form = AccountForm(instance=user)

    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'mobile/account_settings.html', context)