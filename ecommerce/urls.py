from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),


    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/buyers/', views.admin_buyers, name='admin_buyers'),
    path('admin/buyers/<str:option>/', views.admin_buyers, name='admin_buyers'),

    path('admin/sellers/', views.admin_sellers, name='admin_sellers'),
    path('admin/sellers/<str:option>/', views.admin_sellers, name='admin_sellers'),

    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/products/<str:option>/', views.admin_products, name='admin_products'),
    path('admin/addproducts/', views.admin_addproduct, name='admin_addproduct'),
    path('admin/removeproducts/', views.admin_removeproduct, name='admin_removeproduct'),


    path('seller/all_products/', views.seller_all_products, name='seller_all_products'),
    path('seller/registration/', views.seller_registration, name='seller_registration'),
    path('search/',views.SearchProductListView.as_view(),name="search_results")
]  
