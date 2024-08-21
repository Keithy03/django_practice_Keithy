from django import forms
from djgentelella.forms.forms import GTForm
from djgentelella.widgets import core as genwidgets
from rest_framework.exceptions import ValidationError
from atm.models import Customer, User


# TRANSACTION
class TransactionForm(forms.Form):
    pin = forms.CharField(max_length=5,
                          widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter your PIN'}))
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))


# Customers
class LoginForm(GTForm):
    name = forms.CharField(required=True, label='Username', widget=genwidgets.TextInput())
    pin = forms.CharField(required=True, label='Password', widget=genwidgets.PasswordInput())

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'pin', 'money']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),
            'pin': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter a secure PIN'}),
            'money': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter initial balance'}),
        }


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'money']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter customer name'}),
            'money': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter initial balance'}),
        }

