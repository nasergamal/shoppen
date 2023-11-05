from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import Review
# Create your views here.

@login_required
def new_review(request, slug, id):
    if request.method == "POST":
        rating = request.POST.get('rating')
        text = request.POST.get('text')
        title = request.POST.get('title')
        rev = Review.objects.create(user=request.user, product_id=id, rating=rating, title=title, text=text)
    return HttpResponseRedirect(reverse('main:product', kwargs={'cat_slug': slug, 'id': id}))
    