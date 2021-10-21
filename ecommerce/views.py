from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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
