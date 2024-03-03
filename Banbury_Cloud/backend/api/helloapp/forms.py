from django import forms

class UserForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
class UserProfileForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, required=False)
    last_name = forms.CharField(label='Last Name', max_length=100, required=False)
    phone_number = forms.CharField(label='Phone Number', max_length=15, required=False)
    email = forms.EmailField(label='Email', required=False)
