
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms import widgets
from django.http import request

from ecommerce.models import Product, ShippingAddress


class BuyerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=256, required=True)
    gst_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        labels = {"company_name": "Company Name", "gst_number": "GST Number"}
        fields = ('username', 'email', 'password1',
                  'password2', 'company_name', 'gst_number')


class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address1', 'address2', 'city', 'country', 'zipcode')


class AddProductForm(forms.ModelForm):
    # submit_images = forms.ImageField(widget=forms.FileInput(attrs={'multiple':True}), required=True)
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'quantity',"seller", "category"]
        exclude=["seller"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }
    
