from django.shortcuts import render, redirect 
from django.http import HttpResponse
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
from .filters import *
from .decorators import unauthenticated_user, allowed_users, admin_only

import random
import string
import colorsys
import json

def randomString():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(12))

def time_now():
    #current_time = datetime.datetime.now()+datetime.timedelta(hours=16)
    current_time = datetime.datetime(2020, 8, 24)
    
    
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

class graph:
    def __init__(self,machine,time_range,**kwargs):
        self.unit_list = []
        self.no_data = True
        self.data_list = []

        if machine == "All" or machine == "all" or machine == None:
            if "Line" in kwargs:
                self.data_objs = LogData.objects.filter(DateCreated__range=time_range, Machine__Line=kwargs["Line"])
                machine_objs = MachineData.objects.filter(Line = kwargs["Line"])
            else: 
                self.data_objs = LogData.objects.filter(DateCreated__range=time_range)
                machine_objs = MachineData.objects.all()
        else:
            machine_obj = MachineData.objects.get(Code = machine)
            self.data_objs = LogData.objects.filter(Machine=machine_obj,DateCreated__range=time_range)
            machine_objs = MachineData.objects.filter(Code = machine)

        for machine_obj in machine_objs:
            unit = machine_obj.Unit.upper()
            if unit not in self.unit_list:
                self.unit_list.append(unit)

        for unit in self.unit_list:
            self.data_list.append({})
            
        if len(self.data_objs)>0:
            self.no_data = False
            for k,obj in enumerate(self.data_objs):
                if obj.Machine.Unit in self.unit_list:
                    i = self.unit_list.index(obj.Machine.Unit)
                    if obj.Machine.Code in self.data_list[i]:
                        self.data_list[i][obj.Machine.Code].append(round(float(obj.Value),2))
                    else:
                        self.data_list[i][obj.Machine.Code] = [round(float(obj.Value),2)]

        self.charts = []
        self.title_list = []
        self.xs = {} # get time (x-axis)
        if "DateRange" in kwargs:
            for k,obj in enumerate(self.data_objs):
                if k == 0:
                    self.xs[obj.Machine.Code] = [str(obj.DateCreated)]
                elif obj.Machine.Code in self.xs:
                    self.xs[obj.Machine.Code].append(str(obj.DateCreated))
                else:
                    pass
            #print(self.xs)
        else:
            for k,obj in enumerate(self.data_objs):
                if k == 0:
                    self.xs[obj.Machine.Code] = [str(obj.DateCreated).split(" ")[-1]]
                elif obj.Machine.Code in self.xs:
                    self.xs[obj.Machine.Code].append(str(obj.DateCreated).split(" ")[-1])
                else:
                    pass
        self.x = [] # convert to list form
        for ob in self.xs:
            for i in self.xs[ob]:
                self.x.append(i.split(".")[0])
        #print(self.data_list)

    def generate_chart(self,title,code,upper_limit,lower_limit):
        self.title_list.append(title)
        self.charts.append({"data":[],"minmax":[0,1],"title":title})
        if upper_limit != False:
            limit = []
            for x in self.x:
                limit.append(round(float(upper_limit),2))
            self.charts[-1]["data"].append([limit,[100,10,10],"Upper Limit"])
        if lower_limit != False:
            limit = []
            for x in self.x:
                limit.append(round(float(lower_limit),2))
            self.charts[-1]["data"].append([limit,[140,10,10],"Lower Limit"])
        for no,data_dict in enumerate(self.data_list):
            for k,rw in enumerate(data_dict):
                if "list" in str(type(code)) and rw in code:
                    trig = True
                elif code == rw:
                    trig = True
                else:
                    trig = False
                if trig == True:
                    if self.charts[-1]["minmax"][0]>min(data_dict[rw]):
                        self.charts[-1]["minmax"][0] = min(data_dict[rw])
                    if self.charts[-1]["minmax"][1]<max(data_dict[rw]):
                        self.charts[-1]["minmax"][1] = max(data_dict[rw])*1.2

                    if lower_limit != False:
                        if self.charts[-1]["minmax"][0]>lower_limit:
                            self.charts[-1]["minmax"][0] = lower_limit*0.9
                    if upper_limit != False:
                        if self.charts[-1]["minmax"][1]<upper_limit:
                            self.charts[-1]["minmax"][1] = upper_limit*1.1

                    clr = hsv2rgb(float(k)/float(len(data_dict)),1.0,1.0)
                    self.charts[-1]["data"].append([data_dict[rw],list(clr),rw])
                    
        

    def generate_table(self):
        self.tables = [[],[]] #[0] = para , [1] = data rw
        if len(self.data_objs)>0:
            self.no_data = False
            self.tables[0] = self.data_objs[0].parameter()
            for k,obj in enumerate(self.data_objs):
                list_buff = obj.list()
                list_buff[3] = round(float(list_buff[3]),2)
                self.tables[1].append(list_buff)
    


@login_required(login_url='login')
@admin_only
def home(request):
    user = request.user
    record_action(request.user,"Home")
    if user.is_admin or user.is_staff:
        current_time = time_now()
        time_range=[current_time-datetime.timedelta(hours=12),current_time]
        datas = graph("All",time_range)

        wanted_list = ["TEE-901","TE-411","PT-402A"]
        objs = MachineData.objects.all()
        for obj in objs:
            if obj.Code in wanted_list:
                if "-" not in obj.low_limit:
                    low_limit = float(obj.low_limit)
                else:
                    low_limit = False
                if "-" not in obj.upper_limit:
                    upper_limit = float(obj.upper_limit)
                else:
                    upper_limit = False
                #print(upper_limit, low_limit)
                datas.generate_chart(obj.Line+" Line : "+obj.Name+" : "+obj.Parameter+" "+obj.Code+" ("+obj.Unit+")",obj.Code,upper_limit,low_limit)
        
        datas.generate_table()
        if len(datas.tables[1])>200:
            datas.tables[1] = datas.tables[1][-200:]
        # add in ticket
        tickets = []
        #objs_dict = LogData.objects.filter(Machine__Page="MetalDect")
        objs = MachineData.objects.filter(Page="MetalDect")
        #print(objs)
        #objs_dict = {}
        for obj in objs:
            tickets.append([obj.Name,LogData.objects.filter(Machine=obj,DateCreated__range=time_range).count()])
        #print(objs_dict)
        #print(tickets)


        context = {'data':datas.tables,'NoData':datas.no_data, 'charts':datas.charts, 'x':datas.x, 'tickets':tickets}
    
    else:
        tables = [[],[]]
        context = {'data':[[],[]],'NoData':True, 'charts':[], 'x':[], 'ticket':[]}


    return render(request, 'accounts/dashboard.html', context)

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
        machine = request.POST.get('Machine')
        date1 = request.POST.get('date1')
        if date1 == '':
            date1 = '2020-01-01'
        date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
        date2 = request.POST.get('date2')
        if date2 == '':
            date2 = '2120-01-01'
        record_action(request.user,"View "+machine+" Machine Data "+str(date1)+" to "+str(date2))
        date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')

        time_range=[date1,date2+datetime.timedelta(hours=24)]
        if date2 == date1:
            datas = graph(machine,time_range,Line=line,DateRange=True)
        else:
            datas = graph(machine,time_range,Line=line,DateRange=True)
        datas.generate_table()

        if "All" in machine or "all" in machine:
            objs = MachineData.objects.filter(Line=line)
        else:
            objs = MachineData.objects.filter(Code=machine)
        for obj in objs:
            if "-" not in obj.low_limit:
                low_limit = float(obj.low_limit)
            else:
                low_limit = False
            if "-" not in obj.upper_limit:
                upper_limit = float(obj.upper_limit)
            else:
                upper_limit = False
            #print(upper_limit, low_limit)
            datas.generate_chart(obj.Line+" Line : "+obj.Name+" : "+obj.Parameter+" "+obj.Code+" ("+obj.Unit+")",obj.Code,upper_limit,low_limit)
        
        header = [line+" Line Data","Graphical Data from "+str(date1)+" to "+str(date2+datetime.timedelta(hours=24)),"Tabulated Data"]
        
        context = {'data':datas.tables,'NoData':datas.no_data,'Header':header,'x':datas.x,'charts':datas.charts}

        return render(request, 'CRUD/tabulate.html', context)
    else:
        machine_list = []
        machine_obj = MachineData.objects.filter(Line=line)
        for mac in machine_obj:
            machine_list.append([mac.Code,mac.Name])
        machine_list.sort()
        header = [line+" Line","Data Analysis","Data Filter"]
        context = {'Machine':machine_list,'Header':header,"Line":line}#'statuses':statuses, 'tables':tables}

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
@admin_only
def data_plot(request,datatype,daytype):
    user = request.user
    record_action(request.user,"View "+str(datatype)+" Plot Data "+str(daytype))
    datatype = datatype.upper()
    if user.is_admin or user.is_staff:
        current_time = time_now()
        time_range=[current_time-datetime.timedelta(hours=24),current_time]
        datas = graph("all",time_range)
        title_respective = {"KG/HOUR":"","BAR":"Pressure","RPM":"Motor Speed","C":"Temperature","KG":"Quantity"}
        datas.generate_chart(title_respective)

        buff_charts =[]
        trig = False
        for crt_group in datas.charts:
            if datatype in crt_group['title'].upper():
                chart_group = crt_group['data']
                minmax = crt_group['minmax']
                trig = True
                break

        if trig == True:
            for crt in chart_group:
                page = MachineData.objects.get(Code = crt[2]).Page
                buff_charts.append({"data":[crt],"minmax":minmax,"title":"Recorded " + page + " (" + crt[2] + ") "+ datatype +" Graph"})
            charts = buff_charts
        else:
            charts = []
    context = {'NoData':datas.no_data, 'charts':charts, 'x':datas.x}

    return render(request, 'CRUD/plot.html', context)



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
@csrf_exempt
def iotcore(request):
    if request.method == 'POST':
        result = False
        trig = False
        try:
            dev_str = request.GET['dev']
            dev_obj = IOTDev.objects.get(Site=dev_str)
            passport = dev_obj.Passport
            csrf = dev_obj.CSRFTok
            password = passport+":"+csrf
            if 'password' in request.POST:
                parsedJSON = request.POST
            else:
                for strJSON in request.POST:
                    parsedJSON = json.loads(strJSON)
                    break
            upload_password = parsedJSON['password']
            if password == upload_password:
                trig = True
        except Exception as e:
            print(e)
            return render(request, 'accounts/iotcore.html',{"result":result})
        if trig == True:
            try:
                #print("trigger")
                data_list = parsedJSON['data'].split("@@")
                #print(data_list)
                for d in data_list[0:-1]:
                    data = d.split("#")
                    machine = MachineData.objects.get(Address=data[0],IP=data[2])
                    value = round(float(data[1]),2)
                    try:
                        current_time = time_now()
                        splitted_time = str(current_time).split(":")
                        minute = round(int(splitted_time[1]),-1)
                        current_time = splitted_time[0]+":"+str(minute)+":00"
                        current_time = datetime.datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
                    except Exception as e:
                        current_time = time_now()
                    log_obj = LogData(Value = value, Machine = machine, DateCreated = current_time)
                    log_obj.save()
                    machine.LastEdit = current_time
                    machine.save()
                    dev_obj.LastSeen = current_time
                    dev_obj.save()

                if 'message' in parsedJSON:
                    msg = parsedJSON['message']
                    if len(msg) > 5 and msg != 'None':
                        msg_obj = Message(msg = msg)
                        msg_obj.date_created = current_time
                        msg_obj.save()

                result = True
            except Exception as e:
                print(e)
                return render(request, 'accounts/iotcore.html',{"result":result})
        
    else:
        result = False
        req = request.GET
        if "dev" in req:
            try:
                result = randomString()
                dev_str = request.GET['dev']
                dev_obj = IOTDev.objects.get(Site=dev_str)
                dev_obj.CSRFTok = result
                dev_obj.save()
                result += "#"
                addr_list = []
                addr_objs = MachineData.objects.filter(Dev = dev_str)
                for obj in addr_objs:
                    result += obj.Address 
                    result += ":" 
                    result += obj.Line 
                    result += ":" 
                    result += obj.IP 
                    result += "@"
            except Exception as e:
                print(e)
    return render(request, 'accounts/iotcore.html',{"result":result})
