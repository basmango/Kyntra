from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from ecommerce.models import UserProfile
from .forms import SignUpForm

def update_user_data(user, phone):
    UserProfile.objects.update_or_create(user=user, defaults={'phone': phone})
 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            update_user_data(user, form.cleaned_data.get('phone'))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'


def index(request):
    return render(request,'general/home.html')

def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html', {'name':'admin_dashboard'})

def admin_buyers(request):
    return render(request,'admin/admin_buyers.html', {'name':'admin_buyers'})

def admin_sellers(request):
    return render(request,'admin/admin_sellers.html', {'name':'admin_sellers'})

def admin_products(request):
    return render(request,'admin/admin_products.html', {'name':'admin_products'})
