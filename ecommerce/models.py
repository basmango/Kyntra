from django.db import models
from django.conf import settings
# Create your models here.


class ShippingAddress(models.Model):
    address1 = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    # TODO Change to dropdown fields for states and countries
    country = models.CharField(max_length=120)
    zipcode = models.CharField(max_length=120)

    def __str__(self):
        return self.address1 + self.address2 + self.country


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.PositiveSmallIntegerField(default=0)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # phone = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.ImageField(
        upload_to="media", blank=True, null=True)

    def __str__(self):
        return self.user.username


class Buyer(UserProfile):
    address = models.OneToOneField(ShippingAddress, on_delete=models.CASCADE)

    def __str__(self):
        return "Buyer " + self.user.username


class Seller(UserProfile):

    company_name = models.CharField(max_length=100, blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    applied = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    document=models.FileField()
    def __str__(self):
        return "Seller " + self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0)
    payment_completed = models.BooleanField(default=False)
    payment_failed = models.BooleanField(default=False)
    stripe_client_secret = models.CharField(
        max_length=150, blank=True, null=True)
    stripe_payment_intent = models.CharField(
        max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
