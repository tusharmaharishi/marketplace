from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Enter username',
                               widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'tp33'}), required=True)
    password = forms.CharField(label='Enter password',
                               widget=forms.TextInput(attrs={'id': 'password', 'placeholder': '********'}),
                               required=True)


class UserRegistrationForm(forms.Form):
    name = forms.CharField(label='Enter your full name',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thomas Pinckney'}))
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
    driver = forms.CharField(widget=forms.TextInput(attrs={'id': 'driver', 'placeholder': 'Driver id, e.g. 4'}))
    cost = forms.CharField(widget=forms.TextInput(attrs={'id': 'cost', 'placeholder': 'Decimal only, e.g. 1.50'}))
    location_start_lat = forms.CharField(initial=38.853183, widget=forms.TextInput(attrs={'id': 'location_start_lat'}))
    location_start_lon = forms.CharField(initial=38.853183, widget=forms.TextInput(attrs={'id': 'location_start_lon'}))
    location_end_lat = forms.CharField(initial=-77.299025, widget=forms.TextInput(attrs={'id': 'location_end_lat'}))
    location_end_lon = forms.CharField(initial=-77.299025, widget=forms.TextInput(attrs={'id': 'location_end_lon'}))
    time_leaving = forms.CharField(initial="2017-04-05 16:45:00", widget=forms.TextInput(attrs={'id': 'time_leaving'}))
    time_arrival = forms.CharField(initial="2017-04-06 19:05:00", widget=forms.TextInput(attrs={'id': 'time_arrival'}))
