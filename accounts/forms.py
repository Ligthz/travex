from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from decimal import Decimal

from .models import *
from .my_db import *
"""
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['DeliveryDate', 'status','is_paid','DueDate']

class OrderItemForm(ModelForm):
    Item1 = forms.ModelChoiceField(queryset=Product.objects.all(), required = False)
    Bal1 = forms.IntegerField(initial=0, required=False)
    Qty1 = forms.IntegerField(initial=0, required=False)
    RSP1 = forms.FloatField(initial=0.00, required=False)
    RCP1 = forms.FloatField(initial=0.00, required=False)
    DQty1 = forms.FloatField(initial=0.00, required=False)
    DFP1 = forms.FloatField(initial=0.00, required=False)
    UAD1 = forms.DecimalField(initial=0.00, required=False)
    Remark1 = forms.CharField(required=False)
    #Remark = forms.CharField(required = False)
    class Meta:
        model = OrderItem
        fields = ['Item1', 'Bal1','Qty1','RSP1','RCP1','DQty1','DFP1','UAD1','Remark1']

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.fields['Item1'].widget.attrs.update({'style' : 'width:12ch'})
        self.fields['Bal1'].widget.attrs.update({'style' : 'width:4ch'})
        self.fields['Qty1'].widget.attrs.update({'style' : 'width:4ch'})
        self.fields['RSP1'].widget.attrs.update({'style' : 'width:8ch'})
        self.fields['RCP1'].widget.attrs.update({'style' : 'width:8ch'})
        self.fields['DQty1'].widget.attrs.update({'style' : 'width:5ch'})
        self.fields['DFP1'].widget.attrs.update({'style' : 'width:5ch'})
        self.fields['UAD1'].widget.attrs.update({'style' : 'width:8ch'})
        self.fields['Remark1'].widget.attrs.update({'style' : 'width:10ch'})
        self.fields['Remark1'].widget.attrs.update({'placeholder' : '-'})
"""

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'phone','profile_pic']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username', 'name', 'phone', 'password1', 'password2']

