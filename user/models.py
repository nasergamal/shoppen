from django.db import models
from main.models import Product
from django.contrib.auth.models import User

# Create your models here.

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product)
  
    def __str__(self):
      return f'{self.user.username}\'s wishlist'