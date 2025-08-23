from django.contrib import admin 

from core.apps.orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['unity', 'project', 'wherehouse', 'currency']
