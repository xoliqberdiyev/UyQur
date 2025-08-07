from django.contrib import admin 

from core.apps.shared.models import Region, District


class DistrictInline(admin.TabularInline):
    model = District
    extra = 0
    show_change_link = True
    show_full_result_count = True


@admin.register(Region)
class ReginAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [DistrictInline]
    

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']