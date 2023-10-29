from django.db import models
from main.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    delivery_status = [
            ('Pending', "Pending"), ('Confirmed', "Confirmed"),
            ('Shipping', "Shipping"), ('Delivered', "delivered"),
            ('Canceled', 'Canceled')
            ]
    payment_method = [ ('Cash', 'Cash'), ('Credit card','Credit card'),]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    shipping_address = models.CharField(max_length=128)
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=delivery_status, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    payment = models.CharField(max_length=12, choices=payment_method, )
    
    @property
    def total(self):
        '''return total price for all ordered items'''
        items = self.order_items.all()
        total = sum([item.price * item.quantity for item in items])
        return total + 10 # shipping fees. Change to a variable later

    @property
    def item_count(self):
        '''return total count of items ordered'''
        items = self.order_items.all()
        count = sum([item.quantity for item in items])
        return count
    
    def __str__(self):
        return (f'{self.id} {self.user.username}: ${self.total}')
    
        
        
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField(default=0)
    
    @property
    def full_price(self):
        return (self.product.price * self.quantity)