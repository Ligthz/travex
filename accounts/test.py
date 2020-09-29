from accounts.models import *

#PASTUER,FIC-501,db23#112#r,LITER/HOUR
def my_update_db():
    print("started update")
    line = "Line2"
    ip = "192.168.1.199"
    with open("C:\\Users\\YeTien\\Desktop\\Project Report\\FGV Monitoring\\test.txt","r") as opf:
        for rw_list in opf:
            rw = rw_list.split(",")
            addr_list = rw[2].split("#")
            addr = addr_list[0]+"."+addr_list[1]+",r"
            obj = MachineData(
                IP=ip,
                Line = line,
                Page=rw[0],
                Code=rw[1],
                Address = addr,
                Unit = rw[3].rstrip("\n"),
                Dev="IOT"
            )
            obj.save()
            print(obj)


def change_line():
    print("started update")
    line = {"Line1":"Mar","Line2":"Shor"}
    for l in line:
        objs = MachineData.objects.filter(Line = l)
        for obj in objs:
            obj.Line = line[l]
            obj.save()
            print(obj,obj.Line)



def read_list():
    print("started reading")
    data = []
    with open("C:\\Users\\YeTien\\Desktop\\Project Report\\FGV Monitoring\\list.csv", 'r') as opf:
        for rw in opf:
            rw_data = rw.split(',')
            data.append([])
            if "Shor" in rw_data[0]:
                rw_data[0] = "Shortening"
            elif "Mar" in rw_data[0]:
                rw_data[0] = "Margarine"
            elif "MetalDect" in rw_data[0]:
                rw_data[0] = "MetalDector"
            else:
                pass
            for d in rw_data:
                data[-1].append(d.rstrip("\n"))

    complete_list = []
    fail_list = []
    for rw in data:
        try:
            obj = MachineData.objects.get(Code=rw[2])
            complete_list.append(rw[2])
            obj.Line = rw[0]
            if "PASTEUR" in rw[1]:
                rw[1] = "PASTUER"
            obj.Page = rw[1]
            obj.Name = rw[3]
            if "Load" in rw[4]:
                rw[4] = "Load Cell"
            obj.Parameter = rw[4]
            obj.Unit = rw[5]
            obj.low_limit = rw[7]
            obj.upper_limit = rw[6]
            obj.save()
            print(rw)
        except Exception:
            print("Cant found ",rw[2])
            fail_list.append(rw[2])

    objs = MachineData.objects.all()
    for obj in objs:
        if obj.Code not in complete_list:
            print("Obj ",obj," not in list.")

    for rw in fail_list:
        print("Cant found ",rw)
    #line = {"Line1":"Mar","Line2":"Shor"}
    #for l in line:
    #    objs = MachineData.objects.filter(Line = l)
    #    for obj in objs:
    #        obj.Line = line[l]
    #        obj.save()
    #        print(obj,obj.Line)
