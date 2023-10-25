from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse
from django.views import View 
from .models import Product, Category, SubCategory, Brand
from .forms import new_product
from django.conf import settings
from django.contrib import messages
# Create your views here.

def home(request):
    # category = Category.objects.all()
    return render(request, 'index.html')

def category(request, cat_slug):
    category =Category.objects.filter(slug=cat_slug)
#    return render(request, 'main/category.html', context={'category': category})
    if(category):
        products = Product.objects.filter(category__slug=cat_slug)
        context={'products': products, 'category': category.first()}
        return render(request, 'main/category.html', context)
    else:
        messages.error(request, 'Wrong category')
        # return HttpResponseNotFound()
        # return redirect('main:home')


def product(request, cat_slug, id):
    category =Category.objects.filter(slug=cat_slug)
#    return render(request, 'main/category.html', context={'category': category})
    if(category):
        product_info = Product.objects.filter(category__slug=cat_slug, id=id).first()
        amount = range(1, product_info.stock + 1) if product_info.stock > 0 else 0
        context={'product': product_info, 'amount': amount}
        return render(request, 'main/product.html', context)
    else:
        return redirect('main:home')
    
def add_product(request):
    '''django view responsible for the addition of new products'''
    form = new_product()
    if request.method == "POST":
        form = new_product(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            if product.stock <= 0:
                product.instock = False
            product.save()
        else:
            print(form.errors)
    return render(request, 'main/new_product.html', {'form': form})

def update_product(request, id):
    '''django view responsible for the addition of new products'''
    product = get_object_or_404(Product, id=id)
    form = new_product(instance=product)
    if request.method == "POST":
        form = new_product(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            if product.stock <= 0:
                product.instock = False
            product.save()
        else:
            print(form.errors)
    return render(request, 'main/new_product.html', {'form': form})


def get_subcategory(request):
    '''
        responsible for the addition of subcategory based on selected Category in new products page,
        handled by javascript to allow dynamic change in dropdown list of subcategories
    '''
    if request.method == "POST":
        print('OK')
        if request.POST.get('sign') == 'not_shoppen':
            id = request.POST.get('id')
            sub = SubCategory.objects.filter(category__id=id).values('id', 'name')
            return JsonResponse({'result': 's', 'sub': list(sub)})
    
        