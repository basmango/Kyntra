"""fcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ecommerce.views import SignUpView, editProfileView, signup, buyer_signup, seller_signup, ProductDetailView, otp_verification, redirect_user, deleteAccount, deleteAccountRequest

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/signup/', signup, name="signup"),
    path('accounts/signup/buyer', buyer_signup, name="buyer_signup"),
    path('accounts/verify', otp_verification, name="otp_verification"),
    path('redirect_user/', redirect_user, name="redirect_user"),
    path('accounts/signup/seller', seller_signup, name="seller_signup"),
    path('settings/', editProfileView, name="edit_profile"),
    path('accounts/delete/', deleteAccount, name="delete_account"),
    path('accounts/delete-request/', deleteAccountRequest,
         name="delete_account_request"),
    path('kyntra/', include('ecommerce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
