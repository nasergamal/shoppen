from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, SubCategory, Brand
from .forms import new_product


def home(request):
    '''Render Homapage'''
    return render(request, 'index.html')


def category(request, cat_slug):
    '''Render category's products page'''
    category = get_object_or_404(Category, slug=cat_slug)
    context = filtering(request, cat_slug=cat_slug)
    context['category'] = category
    return render(request, 'main/category.html', context)

def search(request):
    '''handle product search requests'''
    name = request.GET.get('query')
    context = filtering(request, name=name)
    if not context:
        messages.info(request, 'No match found')
        return render(request, 'index.html')
    context['slug'] = name
    return render(request, 'main/search.html', context)
    
def filtering(request, cat_slug=None, name=None):
    '''handle products filtering and ordering'''
    order = {"Newest": ['-updated', 'Newest'], "Oldest": ['updated', 'Oldest'],
             "Lowest": ['price', 'Price: low to High'], "Highest": ['-price', 'Price: High to low']}
    br = request.GET.get('brand', None)
    sort = request.GET.get('sort', 'Newest')
    queries = {}
    if cat_slug:
        queries['category__slug'] = cat_slug
        queries['instock'] = True
    elif 'category' in request.GET:
        queries['category'] = request.GET.get('category')
    if name:
        queries['name__icontains'] = name
    queries['active'] = True
    products = Product.objects.filter(**queries).order_by(order[sort][0])
    if not products:
        return None
    price = products.values('price').order_by('price')
    price = [int(price.first()['price']), int(price.last()['price'])]
    price.extend([int(request.GET.get('start', price[0])), int(request.GET.get('end', price[1]))])
      
     
    if price[0] < price[2] or price[1] > price[3]:
        'filter products by price'
        products = products.filter(Q(price__gte=price[2]) & Q(price__lte=price[3]))
    subcategories = SubCategory.objects.filter(id__in=products.values('subcategory').distinct())
    brands = Brand.objects.filter(id__in=products.values('brand').distinct())
    queries = {}
    if 'subcategory' in request.GET:
        'filter by subcategory if required and determine get products prices'
        sub = request.GET.get('subcategory')
        queries['subcategory__in'] = sub.split('_')
        for subcategory in subcategories:
            setattr(subcategory, 'checked', True if str(subcategory.id) in queries['subcategory__in'] else False)
    if br:
        'handle brands in Get parameters and filter'
        queries['brand__in'] = br.split('_')
        for brand in brands:
            setattr(brand, 'checked', True if str(brand.id) in queries['brand__in'] else False)
    products = products.filter(**queries)
    if products:
        price = products.values('price').order_by('price')
        price = [int(price.first()['price']), int(price.last()['price'])]
        price.extend([int(request.GET.get('start', price[0])), int(request.GET.get('end', price[1]))])
    
    page_number =  request.GET.get('page', 1)
    paginator = Paginator(products, 20)
    products = paginator.get_page(page_number)
    products.elided = paginator.get_elided_page_range(number=page_number, 
                                           on_each_side=1,
                                           on_ends=1)
    return {'products': products, "brands": brands, "price": price, 'sort': order[sort][1], 'subcategories': subcategories}    

def product(request, cat_slug, id):
    '''Render product page'''
    category = Category.objects.filter(slug=cat_slug)
    if(category):
        product_info = Product.objects.filter(category__slug=cat_slug, id=id).first()
        amount = range(1, product_info.stock + 1) if product_info.stock > 0 else 0
        wish = False
        if request.user.is_authenticated:
            if request.user.wishlist.products.filter(id=product_info.id):
                wish = True
        context={'product': product_info, 'amount': amount, 'wish': wish}
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
        responsible for the addition of subcategories based on selected Category in product creation/editing page,
        handled by javascript to allow dynamic change in dropdown list of subcategories
    '''
    if request.method == "POST":
        print('OK')
        if request.POST.get('sign') == 'not_shoppen':
            id = request.POST.get('id')
            sub = SubCategory.objects.filter(category__id=id).values('id', 'name')
            return JsonResponse({'result': 's', 'sub': list(sub)})
    
        