from django.contrib import admin

from ecommerce.models import Buyer, Cart, CartItem, Category, Order, OrderItem, Product, Seller, ShippingAddress, ProductImage, UserProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(ShippingAddress)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImage)
