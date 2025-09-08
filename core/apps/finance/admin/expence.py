from django.contrib import admin

from core.apps.finance.models import Expence


@admin.register(Expence)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'cash_transaction']
    