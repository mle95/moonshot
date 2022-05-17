from django.db import models

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class User_manager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone, balance, password):
        email = self.normalize_email(email)
        User = self.model(email=email, phone=phone, balance=balance)
        User.set_password(password)
        User.save(using=self.db)
        return User

    def create_superuser(self, first_name, last_name, email, phone, balance, password):
        User = self.create_user(first_name=first_name, last_name=last_name, email=email, phone=phone, balance=balance, password=password)
        User.is_superuser = True
        User.is_staff = True
        User.save()
        return User


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    balance = models.IntegerField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["phone", "balance"]
    USERNAME_FIELD = 'email'
    objects = User_manager()

    def __str__(self):
        return self.username


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
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField(
        'MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    bidding = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'


class CustomerModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    street = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=15, blank=True)
    zip_code = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    warnings = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Customer: {self.created_on.strftime("%b %d %I: %M %p")}'
