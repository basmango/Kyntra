from django.contrib import admin
from ecommerce.models import Buyer,Seller,Category,Cart,CartItem,Product,ProductImage
# Register your models here.
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(ProductImage)

