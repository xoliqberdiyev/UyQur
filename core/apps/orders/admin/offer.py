from django.contrib import admin

from core.apps.orders.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'order']
    search_fields = ['phone', 'number', 'price']

