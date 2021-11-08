
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ecommerce.models import ShippingAddress

from django.forms import fields
from django.db.models import fields
from django.forms import widgets
from django.http import request

from ecommerce.models import UserProfile, ShippingAddress, Product, Buyer, Seller


class BuyerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data


class SellerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=256, required=True)
    gst_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        labels = {"company_name": "Company Name", "gst_number": "GST Number"}
        fields = ('username', 'email', 'password1',
                  'password2', 'company_name', 'gst_number')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)

        return self.cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('address1', 'address2', 'city', 'country', 'zipcode')


class AdminAddProductsForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'seller': forms.Select(attrs={'class': 'form-select', }),
            'category': forms.Select(attrs={'class': 'form-select', }),
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            'price': forms.NumberInput(attrs={'class': 'form-control', }),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': "3"}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', }),
            'rating': forms.NumberInput(attrs={'class': 'form-control', }),
        }


class AdminRemoveProductsForm(forms.ModelForm):
    id = forms.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ()


class AdminRemoveBuyersForm(forms.ModelForm):
    id = forms.IntegerField(required=True)

    class Meta:
        model = Buyer
        fields = ()


class AddProductForm(forms.ModelForm):
    # submit_images = forms.ImageField(widget=forms.FileInput(attrs={'multiple':True}), required=True)
    class Meta:
        model = Product
        fields = ['name', 'price', 'description',
                  'quantity', "seller", "category"]
        exclude = ["seller"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }


class AdminSellerActionsForm(forms.ModelForm):
    id = forms.IntegerField(required=True)

    class Meta:
        model = Seller
        fields = ()


class OTPForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['otp', 'email']
        widgets = {
            'otp': forms.NumberInput(),
            'email': forms.EmailInput()
        }


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={"readonly": True}),
            'email': forms.EmailInput(attrs={"readonly": True}),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput()
        }


class SellerProfileForm(forms.ModelForm):
    company_name = forms.CharField(max_length=256, required=True)
    gst_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'company_name', 'gst_number']
        widgets = {
            'username': forms.TextInput(attrs={"readonly": True}),
            'email': forms.EmailInput(attrs={"readonly": True}),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'company_name': forms.TextInput(),
            'gst_number': forms.TextInput()
        }
