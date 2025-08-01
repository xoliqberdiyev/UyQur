from django.contrib import admin

from core.apps.wherehouse.models.stock_movemend import StockMovemend


@admin.register(StockMovemend)
class StockMovemendAdmin(admin.ModelAdmin):
    list_display = ['wherehouse_to', 'wherehouse_from', 'product', 'quantity', 'movemend_type']