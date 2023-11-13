from allauth.account.signals import user_logged_out, user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .cart import CartSession, cart_items_update
from .models import Cart, CartItem

@receiver(user_logged_in)
def cart_login(request, **kwargs):
    '''Update user's Cart database and session content on login'''
    session_cart = request.session._session_cache.get('cart')
    user_cart = request.user.cart
    cart_items_update(user_cart,session_cart)
    new_cart = {}
    for item in user_cart.cart_items.all():    
        new_cart[str(item.product_id)] = item.quantity
    request.session._session_cache['cart'] = new_cart
    print(request.session._session_cache['cart'])

@receiver(user_logged_out)
def cart_logout(request, **kwargs):
    '''Update user's Cart database content before logout'''
    session_cart = request.session['cart']
    user_cart = request.user.cart
    user_cart.cart_items.exclude(product_id__in=session_cart.keys()).delete()
    user_cart.save()
    cart_items_update(user_cart,session_cart)

@receiver(post_save, sender=User)
def cart_creation(sender, instance=None, created=False, **kwargs):
    if created:
        Cart.objects.create(user=instance,)