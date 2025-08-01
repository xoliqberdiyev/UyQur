from django.contrib import admin 

from core.apps.accounts.models.permission import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

