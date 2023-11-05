from .ajax import ajax_login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from checkout.forms import new_address
from checkout.models import Order
from main.models import Address, Product
from vendor.models import Review

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'user/userprofile.html', {'user':user})

@login_required
def wishlist(request):
    wish = request.user.wishlist.products.filter(active=True)
    return render(request, 'user/wishlist.html', {'wishlist':wish})

@login_required
def orders(request):
    order = request.user.orders.all()
    print(order, len(order))
    return render(request, 'user/orders.html', {'orders':order})

@login_required
def order_details(request, id):
    order = get_object_or_404(Order, pk=id, user=request.user)
    return render(request, 'user/order_details.html', {'order':order})

@login_required
def order_cancel(request, id):
    order = get_object_or_404(Order, pk=id, user=request.user)
    stat =['Pending' , 'Confirmed' , 'Shipping']
    if order.status in stat:
        order.status = 'Canceled'
        order.save()
        for item in order.order_items.iterator():
            item.product.stock += item.quantity
            item.product.save()
        messages.success(request,'Order Canceled successfully')
    else:
        messages.info(request,'Something went wrong')
    return HttpResponseRedirect(reverse('user:orders'))

@login_required
def address(request):
    address = request.user.addresses.all()
    return render(request, 'user/address.html', {'addresses':address})

@login_required
def add_address(request):
    form = new_address()
    if request.method == "POST":
        form = new_address(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('user:address'))
        else:
            print(form.errors)
    return render(request, 'user/new_address.html', {'form': form})

@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    form = new_address(instance=address)
    if request.method == "POST":
        form = new_address(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('user:address'))
    else:
        print(form.errors)
    return render(request, 'user/new_address.html', {'form': form})

@login_required
def remove_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return HttpResponseRedirect(reverse('user:address'))

@ajax_login_required
def toggle_wishlist(request):
    print('hehehe')
    if request.method == "POST":
        print(request.POST)
        print(request.POST.__dict__, 'end')
        print(request.POST.get('id'))
        product = get_object_or_404(Product, id=request.POST.get('id'))
        wishlist = request.user.wishlist
        if wishlist.products.filter(id=product.id):
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        # wishlist.save()
        return JsonResponse({'authenticated': True})
    else:
        response = JsonResponse({'authenticated': False, "error": "Something went wrong"})
        response.status_code = 400
        return response

@login_required
def wishlist_page_remove(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=request.POST.productId)
        wishlist = request.user.wishlist
        if wishlist.objects.filter(product=product):
            wishlist.remove(product)
            wishlist.save()
        else:
            messages.info(request, 'Product not in wishlist')     
    else:
        messages.info(request, 'Something went wrong')
        return HttpResponseRedirect(reverse('user:wishlist'))

@login_required
def remove_from_wishlist(request):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return HttpResponseRedirect(reverse('user:address'))

    
@login_required
def reviews(request):
    reviews = request.user.reviews.all()
    return render(request, 'user/reviews.html', {'reviews':reviews})