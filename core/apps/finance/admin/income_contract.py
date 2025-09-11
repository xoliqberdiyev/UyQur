from django.contrib import admin 

from core.apps.finance.models import IncomeContract


@admin.register(IncomeContract)
class IncomeContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'date', 'currency']
    