from django.db import models
#from django.contrib.auth.models import AbstractUser



class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')
    ratings = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    home_delivery = models.BooleanField(default=True)
    home_delivery_completed = models.BooleanField(default=False)
    bidding = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'


class CustomerModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    VIP_status = models.IntegerField(blank=True, null=True)
    warnings = models.IntegerField(blank=True, null=True)
    orders_count = models.IntegerField(default=0, null=False)
    total_spending = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    delivery_fee = models.BooleanField(default=True)

    def __str__(self):
        return f'Customer: {self.created_on.strftime("%b %d %I: %M %p")}'
