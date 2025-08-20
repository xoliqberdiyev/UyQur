from django.contrib import admin 

from core.apps.counterparty.models import Counterparty


@admin.register(Counterparty)
class CounterpartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'person']
    