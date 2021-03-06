from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from decimal import Decimal

from .models import *

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['profit', 'duration','deposit','amount']

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = self.fields['username'].label
        self.fields['name'].widget.attrs['placeholder'] = self.fields['name'].label
        self.fields['phone'].widget.attrs['placeholder'] = self.fields['phone'].label
        self.fields['password1'].widget.attrs['placeholder'] = self.fields['password1'].label
        self.fields['password2'].widget.attrs['placeholder'] = self.fields['password2'].label
        self.fields['bank'].widget.attrs['placeholder'] = self.fields['bank'].label
        self.fields['bank_account'].widget.attrs['placeholder'] = self.fields['bank_account'].label
    class Meta:
        model = Account
        fields = ['username', 'name', 'phone', 'password1', 'password2','bank','bank_account']


