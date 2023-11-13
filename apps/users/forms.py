from django import forms
from django.contrib.auth.models import User
from .models import Volunteer

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()  # Corregido de 'firt_name' a 'first_name'
    last_name = forms.CharField()
    
    email = forms.EmailField()

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")
        
        return cleaned_data

    