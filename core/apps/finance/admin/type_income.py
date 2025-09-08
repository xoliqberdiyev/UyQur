from django.contrib import admin 

from core.apps.finance.models import TypeIncome


@admin.register(TypeIncome)
class TypeIncomeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

