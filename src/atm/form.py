from django import forms
from djgentelella.forms.forms import GTForm
from djgentelella.widgets import core as genwidgets

from atm.models import Client, Account


# TRANSACTION
class TransactionForm(GTForm):
    amount = forms.IntegerField(required=True,
                                widget=genwidgets.NumberInput)
    pin = forms.IntegerField(required=True, widget=genwidgets.PasswordInput)


class LoginForm(GTForm):
    name = forms.CharField(required=True, label='Username', widget=genwidgets.TextInput())
    pin = forms.IntegerField(required=True, label='Password', widget=genwidgets.PasswordInput())


class CLientForm(GTForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'dni']
        widgets = {
            "name": genwidgets.TextInput,
            "email": genwidgets.EmailInput,
            "phone": genwidgets.TextInput,
            "dni": genwidgets.TextInput,
        }


class AccountForm(GTForm, forms.ModelForm):
    class Meta:
        model = Account
        fields = ['client', 'pin', 'money']
        widgets = {
            "client": genwidgets.Select,
            "pin": genwidgets.PasswordInput,
            "money": genwidgets.NumberInput
        }
