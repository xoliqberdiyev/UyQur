from django.contrib import admin 

from core.apps.counterparty.models import Counterparty, CounterpartyFolder


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'type', 'inn']


@admin.register(CounterpartyFolder)
class CounterpartyFolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    