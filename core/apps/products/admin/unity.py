from django.contrib import admin 

from core.apps.products.models.unity import Unity


@admin.register(Unity)
class UnityAdmin(admin.ModelAdmin):
    list_display = ['id','value']
    search_fields = ['value']