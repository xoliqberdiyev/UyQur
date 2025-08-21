from django.contrib import admin

from core.apps.orders.models import Party


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['mediator', 'delivery_date', 'payment_date']
    