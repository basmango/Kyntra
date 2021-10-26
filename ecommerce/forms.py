from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User

from ecommerce.models import ShippingAddress

class BuyerSignUpForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ('username', 'email', 'password1', 'password2')

class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length = 256, required=True)
    gst_number = forms.CharField(max_length = 15, required=True)
    class Meta:
        model = User 
        labels = {"company_name": "Company Name", "gst_number": "GST Number"}
        fields = ('username', 'email', 'password1', 'password2', 'company_name', 'gst_number')


class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address1', 'address2', 'city', 'country', 'zipcode')