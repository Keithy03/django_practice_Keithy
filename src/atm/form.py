from django import forms

from atm.models import Customer


# TRANSACTION
class TransactionForm(forms.Form):
    pin = forms.CharField(max_length=5, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your PIN'}))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))


# Customers
class LoginForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}))
    pin = forms.CharField(max_length=5, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your PIN'}))

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user_type', 'name', 'pin', 'money']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name'
            }),
            'pin': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a secure PIN'
            }),
            'money': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter initial balance'
            }),
        }


