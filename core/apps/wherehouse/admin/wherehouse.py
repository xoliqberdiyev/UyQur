from django.contrib import admin 

from core.apps.wherehouse.models.wherehouse import WhereHouse


@admin.register(WhereHouse)
class WhereHouseAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'address', 'branch']
    search_fields = ['name', 'address']
    list_filter = ['branch']