from django.db import models
from django.conf import settings
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.ImageField(
        upload_to="user_profile/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Buyer(UserProfile):
    address = models.CharField(max_length=100, blank=True, null=True)


class Seller(UserProfile):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


# Rating class for accountability

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class CartItem(models.Model):
    cart = models.ManyToOneRel(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    # payment_completed = models.BooleanField(default=False)
    razorpay_payment_id = models.CharField(
        max_length=50, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class OrderItem(models.Model):
    order = models.ManyToOneRel(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
