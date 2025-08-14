from django.contrib import admin 

from core.apps.products.models.folder import Folder, SubFolder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(SubFolder)
class SubFolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'folder']