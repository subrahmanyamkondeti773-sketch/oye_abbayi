from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    phone_number = forms.CharField(max_length=15, required=True, label='Phone Number')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label='Address')
    pin_code = forms.CharField(max_length=10, required=True, label='PIN Code')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15, required=False, label='Phone Number')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Address')
    pin_code = forms.CharField(max_length=10, required=False, label='PIN Code')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
