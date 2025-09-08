from django.contrib import admin 

from core.apps.finance.models import ExpenceType


@admin.register(ExpenceType)
class ExpenceTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
