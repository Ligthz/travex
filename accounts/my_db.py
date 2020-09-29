from .models import *


def get_all_list(datatype, **kwargs):
    key = eval(datatype)
    if len(kwargs)>0:
        objs = key.objects.filter(**kwargs)
    else:
        objs = key.objects.all()
    parameters = key._meta.get_fields()

    ret_list = []
    for obj in objs:
        ret_list.append(obj.list())
    
    return ret_list

def get_parameter(datatype):
    key = eval(datatype)
    parameters = key._meta.get_fields()

    ret_list = []
    for parameter in parameters:
        para = str(parameter).split(":")[-1]
        para = para.split(".")[-1]
        para = para.rstrip(">")
        ret_list.append(para)
    
    return ret_list

def list_get_col(column,inp, **kwargs):
    ret = []
    for rw in inp:
        ret.append(rw[column])

    if "repeat" in kwargs:
        if kwargs["repeat"] == False:
            buff_ret = []
            for rw in ret:
                if rw not in buff_ret:
                    buff_ret.append(rw)
            ret = buff_ret[:]
    return ret

def to_choice_tuple(inp):
    ret = []
    for choice in inp:
        ret.append(tuple([choice,choice]))
    ret = tuple(ret)
    return ret

def form_to_list(inp):
    ret = []
    for form in inp:
        ret.append([])
        for field in form:
            ret[-1].append(field.value())
    return ret