from django.urls import path
from . import views
app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/', views.add_item, name='add_item'),
    path('dec/', views.decrease_item, name='decrease_item'),
    path('rem/', views.remove_item, name='remove_item'),
]