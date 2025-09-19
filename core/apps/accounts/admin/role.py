from django.contrib import admin

from core.apps.accounts.models.role import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    # autocomplete_fields = ("permissions", "permission_to_tabs", 'permission_to_actions')
    filter_horizontal = ("permissions", "permission_to_tabs", 'permission_to_actions')
    