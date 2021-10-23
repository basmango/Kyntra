from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from ecommerce.models import Buyer, Seller, ShippingAddress, UserProfile
from .forms import AddressForm, BuyerSignUpForm, SellerSignUpForm

def update_user_data(user, phone):
    UserProfile.objects.update_or_create(user=user, defaults={'phone': phone})

def signup(request):
    return render(request, 'registration/signup.html')


def buyer_signup(request):
    if request.method == 'POST':
        form = BuyerSignUpForm(request.POST)
        address_form = AddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            user = form.save()
            address = address_form.save()
            user.refresh_from_db()
            Buyer.objects.create(user=user, address=address)
            user.save()
            address.save()
            raw_password = form.cleaned_data.get('password1')
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)            
            return redirect('index')
    else:
        form = BuyerSignUpForm()
        address_form = AddressForm()

    return render(request,'registration/buyer_signup.html',{'form': form, "address_form": address_form})

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            Seller.objects.create(user=user, company_name=form.cleaned_data.get('company_name'), gst_number=form.cleaned_data.get('gst_number'))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # TODO Change to seller registration for document upload etc.
            return redirect('index')
    else:
        form = SellerSignUpForm()

    return render(request,'registration/seller_signup.html', {'form': form})



def index(request):
    return render(request, 'general/home.html')


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html', {'name': 'admin_dashboard'})


def admin_buyers(request):
    return render(request, 'admin/admin_buyers.html', {'name': 'admin_buyers'})


def admin_sellers(request):
    return render(request, 'admin/admin_sellers.html', {'name': 'admin_sellers'})


def admin_products(request):
    return render(request, 'admin/admin_products.html', {'name': 'admin_products'})


def seller_all_products(request):
    products = [
        {
            "name": "Phone",
            "price": 100,
            "description":"This is a phone",
            "supertag": "SOLD",
            "image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
        },
        {
            "name": "Phone",
            "price": 100,
            "description":"This is a phone",
            "supertag": "SOLD",
            "image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
        },
        
        {
            "name": "Phone",
            "price": 100,
            "description":"This is a phone",
            "supertag": "SOLD",
            "image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
        },
        {
            "name": "Phone",
            "price": 100,
            "description":"This is a phone",
            "supertag": "SOLD",
            "image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
        },
        {
            "name": "Phone",
            "price": 100,
            "description":"This is a phone",
            "supertag": "SOLD",
            "image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
        },
        {
            "name": "Phone",
            "price": 100,
            "description":"This is a phone",
            "supertag": "SOLD",
            "image_uri": "https://media.istockphoto.com/photos/mobile-phone-top-view-with-white-screen-picture-id1161116588?k=20&m=1161116588&s=612x612&w=0&h=NKv_O5xQecCHZic53onobxjqGfW7I-D-tBrzXaPbj_Q="
        },
   
    ]
    return render(request, 'seller/all_products.html', {'name': 'seller_all_products',"products":products})
def seller_registration(request):
    return render(request, 'seller/seller_registration.html', {'name': 'seller_registration'})