from django import forms

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

# class UserSignupForm(forms.Form):
#
#
#
# class NewCarpoolForm(forms.Form):
#
#
# class SearchForm(forms.Form):
