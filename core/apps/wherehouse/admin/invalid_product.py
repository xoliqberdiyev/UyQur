from django.contrib import admin 

from core.apps.wherehouse.models import InvalidProduct


@admin.register(InvalidProduct)
class InvalidProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'inventory', 'project_folder', 'amount', 'status']