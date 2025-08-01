from django.contrib import admin

from core.apps.accounts.models.role import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    