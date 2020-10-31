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

import random
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
            record_action(request.user,"Login")
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
    if request.is_ajax():
        datas = []
        return JsonResponse({"success":True,"datas":datas})
    record_action(request.user,"Home")

    return render(request, 'accounts/dashboard.html')

@login_required(login_url='login')
def userPage(request):
    output_text = "Please await for confirmation for this account after signup..."

    record_action(request.user,"Un-authenticated")
    context = {'output_text':output_text}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@admin_only
def data_landing(request,datatype,line):
    user = request.user
    if request.method == 'POST':
        personal = request.POST.get('Machine')
        date1 = request.POST.get('date1')
        date2 = request.POST.get('date2')
        if date1 == '':
            date1 = '2020-01-01T00:00'

        date1 = datetime.datetime.strptime(date1, '%Y-%m-%dT%H:%M')
        if date2 == '':
            date2 = '2120-01-01T23:59'
        date2 = datetime.datetime.strptime(date2, '%Y-%m-%dT%H:%M')

        time_range=[date1,date2]

        if "All" not in personal:
            data_objs = LogData.objects.filter(DateCreated__range=time_range,PIC=personal)
        else:
            data_objs = LogData.objects.filter(DateCreated__range=time_range)

        datas = [[],[]]
        if len(data_objs) == 0:
            no_data = True
        else:
            no_data = False
        
            para = data_objs[0].parameter()
            data = []
            for obj in data_objs:
                data.append(obj.list())
            datas[0] = para
            datas[1] = data

        header = [line+" Site Data","Logged Data of personal : " +str(personal)+" from "+str(date1)+" to "+str(date2),"Tabulated Data"]
        
        context = {'data':datas,'NoData':no_data,'Header':header}

        return render(request, 'CRUD/tabulate.html', context)
    else:
        personal_list = []
        account_obj = Account.objects.filter(Site=line)
        for personal in account_obj:
            personal_list.append([personal.name, personal.Site])
        personal_list.sort()
        header = [line+" Site","Data Analysis","Data Filter"]
        context = {'Machine':personal_list,'Header':header,"Line":line}#'statuses':statuses, 'tables':tables}

        return render(request, 'CRUD/landing.html', context)



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
