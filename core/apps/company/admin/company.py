from django.contrib import admin 

from core.apps.company.models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']