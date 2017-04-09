from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator



from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)


class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=128)
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128)
    balance = forms.DecimalField(initial=0.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])


class CarpoolListingForm(forms.Form):
    driver = forms.CharField()
    cost = forms.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    location_start_lat = forms.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    location_start_lon = forms.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    location_end_lat = forms.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    location_end_lon = forms.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])
    time_leaving = forms.CharField()
    time_arrival = forms.CharField()