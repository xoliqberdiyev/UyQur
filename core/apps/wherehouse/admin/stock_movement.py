from django.contrib import admin

from core.apps.wherehouse.models.stock_movemend import StockMovemend, StockMovmendProduct


class StockMovemendProductInline(admin.TabularInline):
    model = StockMovmendProduct
    extra = 0
    
    def has_add_permission(self, request, obj):
        return False


@admin.register(StockMovemend)
class StockMovemendAdmin(admin.ModelAdmin):
    list_display = ['id', 'wherehouse_to', 'wherehouse_from', 'movemend_type']
    inlines = [StockMovemendProductInline]


@admin.register(StockMovmendProduct)
class StockMovemendProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'inventory', 'quantity']