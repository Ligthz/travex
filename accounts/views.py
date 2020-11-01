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
            return redirect('home')
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
@csrf_exempt
def home(request):
    user = request.user
    if request.method == 'POST':
        #datas = []
        #return JsonResponse({"success":True,"datas":datas})
        #user_id = request.POST.get('')
        #user = Account.objects.get()
        print(request.POST)
        for submision in request.POST:
            if "Submission-" in submision:
                user_id = int(submision.split("-")[-1])
                user = Account.objects.get(id=user_id)
                break
        return render(request, 'accounts/account_settings.html',{'user':user})

    #record_action(request.user,"Home")

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



@login_required(login_url='login')
@admin_only
def machine(request):
    user = request.user
    record_action(request.user,"View Machine Data")
    tables = [[],[]] #[0] = para , [1] = data rw
    no_data = True
    if user.is_admin or user.is_staff:
        current_time = time_now()
        data_objs = MachineData.objects.all()
        if len(data_objs)>0:
            no_data = False
            tables[0] = data_objs[0].parameter()
            for k,obj in enumerate(data_objs):
                list_buff = obj.list()
                tables[1].append(list_buff)
        header = ["Machine Data","Machine Data Up To Date.","Table of Machine Data"]
    
    else:
        tables = [[],[]]

    context = {'data':tables,'NoData':no_data,'Header':header}

    return render(request, 'CRUD/tabulate.html', context)


@login_required(login_url='login')
def order_information(request,pk):
    user = request.user
    context = {}

    return render(request, 'accounts/Dashboard/order_information.html', context)

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
    return render(request, 'accounts/account_settings.html', context)

# ======================== IOT Core =========================================
def time_formatter(request):
    # remove minute and second
    try:
        if "Time" in request.POST:
            current_time = request.POST.get('current_time')
        else:
            current_time = time_now()
        splitted_time = str(current_time).split(":")
        minute = int(splitted_time[1])
        if minute > 10:
            minute = round(minute,-1)
        current_time = splitted_time[0]+":"+str(minute)+":00"
        current_time = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        current_time = time_now()
    return current_time

def security_check(request):
    try:
        trig = False
        dev_str = request.GET['dev']
        dev_obj = IOTDev.objects.get(Site=dev_str)
        passport = dev_obj.Passport
        csrf = dev_obj.CSRFTok
        password = passport+":"+csrf
        if 'password' in request.POST:
            upload_password = request.POST.get('password')
            if password == upload_password:
                trig = True
                current_time = time_formatter()
                dev_obj.LastSeen = current_time
                dev_obj.save()
        return trig
    except Exception as e:
        return False

@csrf_exempt
def iotcore(request):
    """ POST > Receive data from Device
        request.GET = 
        request.POST = {
            'password':password,
            'data':[{'IP':IP,
                     'Address':Address,
                     'Value':Value
                     },{},...],
            'Time':str(datetime) (**Optional/Only during reupload),
            'message':message (**Optional/Only during error)
        }
        return = {'result':True/False}

        GET > Receive address from Server
        request.GET = {'Dev':Dev_str (IOT)}
        return = {
            'csrf':csrf,
            'data':{
                'ip1':[addr1,addr2,....],
                'ip2':[addr3,addr4,....],...
            }
        }
    """
    if request.method == 'POST':
        try:
            if security_check(request) == True:
                parsedJSON = dict(request.POST)
                data_list = parsedJSON['data']
                start_rec = False # For log data purpose
                for data in data_list:
                    machine = MachineData.objects.get(Address=data["Address"],IP=data["IP"])
                    value = round(float(data["Value"]),2)
                    current_time = time_formatter(request) # If there are "Time" in request.POST, it will be used

                    machine.LastEdit = current_time
                    machine.Value = value
                    machine.save()

                    last_log = LogData.objects.latest('DateCreated')
                    if time_now() - last_log.DateCreated > datetime.timedelta(minutes=10) or start_rec == True:
                        log_obj = LogData(Value = value, Machine = machine, DateCreated = current_time)
                        log_obj.save()
                        start_rec = True
                    
                    # Log message if found message in parsed json
                    if 'message' in parsedJSON:
                        msg = parsedJSON['message']
                        if len(msg) > 5 and msg != 'None':
                            msg_obj = Message(msg = msg)
                            msg_obj.date_created = current_time
                            msg_obj.save()
                return JsonResponse({"result":True})
            else:
                return JsonResponse({"result":False})
        except Exception as e:
            print(e)
            return JsonResponse({"result":False})
        
    else:
        csrf = False
        addr_list = {}
        req = request.GET
        if "dev" in req:
            try:
                csrf = randomString()
                dev_str = request.GET['dev']
                dev_obj = IOTDev.objects.get(Site=dev_str)
                dev_obj.CSRFTok = csrf
                dev_obj.save()
                
                addr_objs = MachineData.objects.filter(Dev = dev_str)
                for obj in addr_objs:
                    if obj.IP in addr_list:
                        addr_list[obj.IP].append(obj.Address)
                    else:
                        addr_list[obj.IP] = [obj.Address]
            except Exception as e:
                print(e)
        return JsonResponse({"csrf":csrf,"data":addr_list})
