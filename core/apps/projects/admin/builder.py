from django.contrib import admin 

from core.apps.projects.models import Builder


@admin.register(Builder)
class BuilderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    