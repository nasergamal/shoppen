# context processors allow access to certain data from any page on website
from .models import Category
from cart.cart import CartSession


def categories(request):
    return {'categories': Category.objects.all()}

def cart(request):
    return {'cart': CartSession(request)}
