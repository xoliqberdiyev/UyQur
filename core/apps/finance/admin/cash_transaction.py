from django.contrib import admin

from core.apps.finance.models import CashTransaction, CashTransactionFolder


@admin.register(CashTransaction)
class CashTransaction(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(CashTransactionFolder)
class CashTransactionFolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']