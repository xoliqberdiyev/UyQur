from django.contrib import admin

from core.apps.orders.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number', 'order']
    search_fields = ['name', 'phone', 'number', 'price']

