from django import forms

from .models import User, Carpool, Authenticator


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'balance', 'carpool_owned', 'carpool_joined']


class CarpoolForm(forms.ModelForm):
    class Meta:
        model = Carpool
        fields = ['driver', 'cost', 'location_start', 'location_end', 'time_leaving', 'time_arrival']


class AuthenticatorForm(forms.ModelForm):
    class Meta:
        model = Authenticator
        fields = ['username', 'authenticator', 'date_created']
