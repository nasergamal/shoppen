from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import new_address
from cart.cart import CartSession
from main.models import Address, Product
from .models import Order, OrderItem

# Create your views here.
@login_required
def checkout(request):
    '''Render HTML page for checkout'''
    address = request.user.addresses.all()
    data = request.session.get('cart', {})
    if len(data) <= 0:
        messages.info(request, 'Cart is empty')
        return HttpResponseRedirect(reverse('main:home'))
    id_list = data.keys() #[i for i in data.keys()]
    items = Product.objects.filter(id__in=id_list)
    for item in items:
        setattr(item, 'amount', data[str(item.id)])
    total = CartSession(request).total_price() + 10
    return render(request, 'checkout/checkout.html', {'addressess': address, 'items': items, 'total': total})

@login_required
def create_order(request):
    '''Create a new row in Order table and related rows in Orderitems table based on users cart'''
    cart = CartSession(request)
    if request.method == "POST" and len(cart) > 0:
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment') 
        id_list = cart.cart.keys()
        items = Product.objects.filter(id__in=id_list)
        change = 0
        for item in items.iterator():
            if item.stock < cart.cart[str(item.id)]:
                cart.cart[str(item.id)] = item.stock
                cart.save()
                changes = 1
                messages.info(request, f'{item.name} stock were insufficent amount modified to {item.stock }')
        if change:
            return HttpResponseRedirect(reverse('checkout:checkout'))
            
        address = Address.objects.get(id=address_id)
        total = cart.total_price() + 10 # shipping fees. Change to a variable later
        order = Order.objects.create(user=request.user, shipping_address=address.address,
                                     phone=address.phone_number,status='Pending', total_price=total,
                                     payment=payment_method)
        
        for item in items:
            OrderItem.objects.create(product=item, order=order, price=item.price ,quantity=cart.cart[str(item.id)])
            item.stock -= cart.cart[str(item.id)]
            if item.stock == 0:
                item.instock = False
            item.save()
        cart.empty(request)
        request.user.cart.cart_items.all().delete()
        messages.success(request, 'order created successfully')
        return HttpResponseRedirect(reverse('user:order_details',kwargs={'id': order.id}))
    elif len(cart) <= 0:
        messages.info(request, 'Cart is empty')
    else:
        messages.info(request, 'Something went wrong')
    return HttpResponseRedirect(reverse('main:home'))
        

@login_required
def checkout_add_address(request):
    '''Address addition from checkout page'''
    form = new_address()
    if request.method == "POST":
        form = new_address(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('checkout:checkout'))
        else:
            print(form.errors)
    return render(request, 'checkout/checkout_new_address.html', {'form': form})

@login_required
def checkout_edit_address(request, id):
    '''Address edit from checkout page'''
    address = get_object_or_404(Address, id=id)
    form = new_address(instance=address)
    if request.method == "POST":
        form = new_address(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return HttpResponseRedirect(reverse('checkout:checkout'))
    else:
        print(form.errors)
    return render(request, 'checkout/checkout_new_address.html', {'form': form})