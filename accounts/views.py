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
from .decorators import unauthenticated_user, allowed_users, admin_only
from crm1.settings import MEDIA_ROOT

import random, datetime
import string
import colorsys
import json
import os


def error_404_view(request,exception):
    return render(request, 'accounts/login/register.html')

def randomString():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(12))

def time_now():
    current_time = datetime.datetime.now()+datetime.timedelta(hours=16)
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
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/login/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #record_action(request.user,"Login")
            user_obj = Account.objects.get(username=username)
            user_obj.last_login = time_now()
            user_obj.save()
            return redirect('control-home')
        else:
            if request.user.is_active == False:
                messages.info(request, 'Please wait for admin to activate your account.')
                return redirect('mobile-home')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    #record_action(request.user,"Logout")
    return redirect('login')

# ======================== Dashboard =========================================        
def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def record_action(user,action):
    user = Account.objects.get(username=str(user))
    action_obj = UserAction(user = user, action = action)
    action_obj.save()

@login_required(login_url='login')
@admin_only
def home(request):
    user = request.user
    
    current_time = time_now()
    day_range = [current_time-datetime.timedelta(days=1),current_time]
    week_range = [current_time-datetime.timedelta(days=7),current_time]
    month_range = [current_time-datetime.timedelta(days=30),current_time]

    daily_user = Account.objects.filter(date_created__range=day_range, is_staff=False, is_active=True).count()
    weekly_user = Account.objects.filter(date_created__range=week_range, is_staff=False, is_active=True).count()
    monthly_user = Account.objects.filter(date_created__range=month_range, is_staff=False, is_active=True).count()

    tickets = [["Daily User",daily_user],["Weekly User",weekly_user],["Monthly User",monthly_user]]

    data = []
    today_login_user = Account.objects.filter(last_login__range=day_range, is_staff=False, is_active=True)
    if today_login_user.count() == 0:
        NoData = True
    else:
        NoData = False
        data.append(today_login_user[0].para())
        data.append([])
        for obj in today_login_user:
            data[1].append(obj.list())

    return render(request, 'accounts/dashboard.html',{'tickets':tickets,'NoData':NoData,'data':data})

@login_required(login_url='login')
def userPage(request):
    output_text = "Please await for confirmation for this account after signup..."

    record_action(request.user,"Un-authenticated")
    context = {'output_text':output_text}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@admin_only
def data_landing(request):
    user = request.user    
    
    data = []
    today_login_user = Account.objects.filter(is_staff=False, is_active=True)
    if today_login_user.count() == 0:
        NoData = True
    else:
        NoData = False
        data.append(today_login_user[0].para())
        data.append([])
        for obj in today_login_user:
            data[1].append(obj.list())


    return render(request, 'accounts/tabulate.html', {'NoData':NoData,'data':data})



# ======================== Account Setting =========================================

def str_to_num(number):
    number = str(round(float(number),2))
    if len(number.split(".")[-1]) == 1:
        number += "0"
    return number

@login_required(login_url='login')
def accountSettings(request,user_id):
    user = request.user
    this_user = Account.objects.get(id=user_id)

    if request.method == 'POST':
        print(request.POST)
        this_user_id = request.POST.get("id")
        this_user = Account.objects.get(id=this_user_id)
        this_user.profit = str_to_num(request.POST.get("profit"))
        this_user.duration = str_to_num(request.POST.get("duration"))
        this_user.deposit = str_to_num(request.POST.get("deposit"))
        this_user.amount = str_to_num(request.POST.get("amount"))
        this_user.save()
        return redirect('control-user')


    return render(request, 'accounts/account_settings.html', {'this_user':this_user})
