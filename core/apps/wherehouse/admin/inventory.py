from django.contrib import admin 

from core.apps.wherehouse.models.inventory import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'wherehouse', 'is_invalid']
    list_filter = ['wherehouse', 'is_invalid']