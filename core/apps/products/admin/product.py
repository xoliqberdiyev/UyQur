from django.contrib import admin

from core.apps.products.models.product import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']