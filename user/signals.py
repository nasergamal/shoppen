from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wishlist

@receiver(post_save, sender=User)
def cart_creation(sender, instance=None, created=False, **kwargs):
    if created:
        Wishlist.objects.create(user=instance,)