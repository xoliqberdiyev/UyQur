from django.contrib import admin

from core.apps.finance.models import CashTransaction


@admin.register(CashTransaction)
class CachTransaction(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']