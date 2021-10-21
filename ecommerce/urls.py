from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/buyers/', views.admin_buyers, name='admin_buyers'),
    path('admin/sellers/', views.admin_sellers, name='admin_sellers'),
    path('admin/products/', views.admin_products, name='admin_products'),

]