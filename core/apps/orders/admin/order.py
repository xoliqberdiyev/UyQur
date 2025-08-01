from django.contrib import admin 

from core.apps.orders.models import Order, OrderApplication


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['quantity', 'product', 'unity', 'project', 'wherehouse']
    list_display = ['unity', 'project', 'wherehouse']


@admin.register(OrderApplication)
class OrderApplicationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'status']
