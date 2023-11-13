from django.db import models
from django.contrib.auth.models import User
from main.models import Product
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    @property
    def item_count(self):
        '''return total count of items ordered'''
        items = self.items.all()
        count = sum([item.quantity for item in items])
        return count
        
        
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField(default=0)
    
    @property
    def full_price(self):
        return (self.product.price * self.quantity)
    
    