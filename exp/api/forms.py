from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)


class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=128)
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)
    balance = forms.DecimalField(initial=0.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
