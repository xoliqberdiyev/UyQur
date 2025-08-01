from django.contrib import admin 

from core.apps.company.models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'company']
    search_fields = ['name', 'location', 'company']
    list_filter = ['company']