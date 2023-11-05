from django.contrib.auth.models import User
from django.db import models
from main.models import Product

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=128)
    updated = models.DateTimeField(auto_now=True)
    rating = models.IntegerField()
    text = models.CharField(max_length=500)
    
    def star_rate(self):
        rate = [1 for i in range(self.rating)]
        for i in range(len(rate), 5):
            rate.append(0)
        return rate