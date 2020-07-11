from django import forms
from .models import *
from .views import *
from django.contrib.auth.models import User



class EditPassword(forms.Form):
    old_password1 = forms.CharField(max_length=64, widget=forms.PasswordInput)
    password1 = forms.CharField(max_length=64, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput)

