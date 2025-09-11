from django.contrib import admin

from core.apps.finance.models import ExpenceContract


class ExpenceContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'date', 'currency']