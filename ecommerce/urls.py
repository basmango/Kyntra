from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]