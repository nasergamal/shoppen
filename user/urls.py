from django.urls import path, include
from . import views
app_name = 'user'

urlpatterns = [
    path('', views.user_profile, name='userprofile'), 
    path('wishlist/', views.wishlist, name='wishlist'), 
    path('wishlist/<int:id>', views.wishlist_page_remove, name='remove_from_wishlist'),
    path('wishlist/modify', views.toggle_wishlist, name='toggle_item'),
    path('orders/', views.orders, name='orders'), 
    path('orders/<int:id>', views.order_details, name='order_details'),
    path('orders/<int:id>/cancel', views.order_cancel, name='order_cancel'),
    path('addresses/', views.address, name='address'), 
    path('address/new', views.add_address, name='new_address'), 
    path('address/edit/<int:id>', views.edit_address, name='edit_address'), 
    path('addresse/remove/<int:id>', views.remove_address, name='remove_address'), 
    path('reviews/', views.reviews, name='reviews')
]