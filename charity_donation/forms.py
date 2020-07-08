from django import forms
from .models import *
from .views import *
from django.contrib.auth.models import User

#
# class BudgetForm(forms.ModelForm):
#     class Meta:
#         model = Budget
#         fields = '__all__'
#     def __init__(self, *args, **kwargs):
#         super(BudgetForm, self).__init__(*args, **kwargs)
#         self.fields['description'].required = False


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']