from django.urls import path
from . import views

app_name='checkout'
urlpatterns = [
    path('', views.checkout ,name='checkout'),
    path('create-order', views.create_order ,name='create_order'),
    path('add-address/', views.checkout_add_address, name='checkout_new_address'),
    path('change-address/<int:id>', views.checkout_edit_address, name='checkout_edit_address'),
]