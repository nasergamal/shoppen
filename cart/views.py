from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import CartSession
from main.models import Product
# Create your views here.

def view_cart(request):
        data = request.session.get('cart', {})
        id_list = data.keys()
        items = Product.objects.filter(id__in=id_list)
        for item in items:
            setattr(item, 'amount', data[str(item.id)])
        return render(request, 'cart/cart.html', {"items": items})

def add_item(request):
    cart = CartSession(request)
    if request.method == "POST":
        if request.POST.get('sign') == 'not_shoppen':
            product = get_object_or_404(Product, id=request.POST.get('id'))
            amount = int(request.POST.get('amount'))
            id = str(product.id)
            cart.add(request, product, amount)
            return JsonResponse({'result': 'success', 'amount': len(cart),
                                 'total': cart.total_price(), 'item': cart.item_quantity(id)})
    return JsonResponse({'result': 'fail'})

def decrease_item(request):
    '''decrease (or remove if 0) item from cart'''
    cart = CartSession(request)
    if request.method == "POST":
        if request.POST.get('sign') == 'not_shoppen':
            product = get_object_or_404(Product, id=request.POST.get('id'))
            id = str(product.id)
            cart.decrement(request, id)
            return JsonResponse({'result': 'success', 'amount': len(cart),
                                 'total': cart.total_price(), 'item': cart.item_quantity(id)})
    return JsonResponse({'result': 'fail'})

def remove_item(request):
    cart = CartSession(request)
    if request.method == "POST":
        if request.POST.get('sign') == 'not_shoppen':
            product = get_object_or_404(Product, id=request.POST.get('id'))
            id = str(product.id)
            cart.remove(request, id)
            return JsonResponse({'result': 'success', 'amount': len(cart),
                                 'total': cart.total_price(),})
    return JsonResponse({'result': 'fail'})