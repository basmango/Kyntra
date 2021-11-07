from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import fields

from ecommerce.models import ShippingAddress, Product

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

class AdminAddProductsForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		widgets = {
            'seller': forms.Select(attrs={'class': 'form-select',}),
            'category': forms.Select(attrs={'class': 'form-select',}),
            'name': forms.TextInput(attrs={'class': 'form-control',}),
            'price': forms.TextInput(attrs={'class': 'form-control',}),
            'description': forms.Textarea(attrs={'class': 'form-control','rows':"3"}),
            'quantity': forms.TextInput(attrs={'class': 'form-control',}),
            'rating': forms.TextInput(attrs={'class': 'form-control',}),
        }