from django import forms

from .models import User, Carpool


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'balance', 'carpool_owned', 'carpool_joined']


class CarpoolForm(forms.ModelForm):
    class Meta:
        model = Carpool
        fields = ['driver', 'cost', 'location_start', 'location_end', 'time_leaving', 'time_arrival']
