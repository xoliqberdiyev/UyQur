from django.contrib import admin 

from core.apps.finance.models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'cash_transaction']
    list_filter = ['cash_transaction', 'payment_type']
