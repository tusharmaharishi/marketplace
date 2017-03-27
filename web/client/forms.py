from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Enter username',
                               widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'tp33'}), required=True)
    password = forms.CharField(label='Enter password',
                               widget=forms.TextInput(attrs={'id': 'password', 'placeholder': '********'}),
                               required=True)


class UserRegistrationForm(forms.Form):
    # first_name = forms.CharField(initial = 'eg. John',widget=forms.TextInput(attrs={'class' : 'form-control'}))
    # last_name = forms.CharField(initial = 'eg. lennon',widget=forms.TextInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(label='Enter username',
                               widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'tp33'}), required=True)
    password1 = forms.CharField(label='Enter password',
                                widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': '********'}),
                                required=True)
    password2 = forms.CharField(label='Retype password',
                                widget=forms.TextInput(attrs={'class': 'input_text', 'placeholder': '********'}),
                                required=True)

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if not pass2:
            raise forms.ValidationError("Please confirm password.")
        if pass1 != pass2:
            raise forms.ValidationError("The passwords entered did not match.")
        return pass2


class CreateCarpoolForm(forms.Form):
    driver = forms.CharField(widget=forms.TextInput(attrs={'id': 'driver'}))
    cost = forms.CharField(widget=forms.TextInput(attrs={'id': 'cost'}))
    location_start = forms.CharField(widget=forms.TextInput(attrs={'id': 'location_start'}))
    location_end = forms.CharField(widget=forms.TextInput(attrs={'id': 'location_start'}))
    time_leaving = forms.CharField(widget=forms.TextInput(attrs={'id': 'time_leaving'}))
    time_arrival = forms.CharField(widget=forms.TextInput(attrs={'id': 'time_arrival'}))
