from django.contrib import admin 

from core.apps.accounts.models.permission import Permission, PermissionToTab, PermissionToAction


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    filter_horizontal = ['permission_tab']

@admin.register(PermissionToTab)
class PermissionToTabAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    filter_horizontal = ['permission_to_actions']


@admin.register(PermissionToAction)
class PermissionToActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']