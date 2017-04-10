from django import forms

from .models import User, Carpool, Authenticator


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'password', 'balance', 'carpool_owned', 'carpool_joined']


class CarpoolForm(forms.ModelForm):
    class Meta:
        model = Carpool
        fields = ['driver', 'cost', 'location_start_lat', 'location_start_lon', 'location_end_lat', 'location_end_lon',
                  'time_leaving', 'time_arrival']


class AuthenticatorForm(forms.ModelForm):
    class Meta:
        model = Authenticator
        fields = ['username', 'auth_token']


# class UserLoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']