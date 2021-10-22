from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length = 11, required=True)
    class Meta:
        model = User 
        labels = {'phone': 'Phone Number'}
        fields = ('username', 'phone', 'password1', 'password2' )
