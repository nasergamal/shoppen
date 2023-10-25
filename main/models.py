from django.db import models
from django.contrib.auth.models import User
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_vendor = models.BooleanField(default=False)
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = PhoneNumberField()
    phone_number2 = PhoneNumberField(null=True)
    address = models.CharField(max_length=256)
    additional_info = models.CharField(max_length=256, null=True)
    class Meta:
        verbose_name_plural = "Addresses"
        

class Category(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    picture = models.ImageField(upload_to="img/category")
    
    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "SubCategories"
    
class Brand(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "Brands"

class Product(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(max_length=4096, null=True)
    picture = models.ImageField(upload_to="img")
    instock = models.BooleanField(default=True)

    def __str__(self):
        return self.name