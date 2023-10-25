from django.contrib import admin
# from django.utils.html import format_html_join
from .models import Order
# Register your models here.
# admin.site.register(Order)
@admin.register(Order)
class Orders(admin.ModelAdmin):
    fields = ('user', 'shipping_address', 'phone', 'status', 'total_price', 'payment', 'updated')
    readonly_fields = ('user', 'total_price', 'updated','payment')