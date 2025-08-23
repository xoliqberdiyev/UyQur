from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse 

from core.apps.shared.models import UsdCourse


@admin.register(UsdCourse)
class UsdCourseAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not UsdCourse.objects.exists()
    
    def has_delete_permission(self, request, obj = ...):
        return False

    def changelist_view(self, request, extra_context=None):
        config, created = UsdCourse.objects.get_or_create(
            defaults=dict(
                value=0
            )
        )
        url = reverse("admin:shared_usdcourse_change", args=[config.id])
        return HttpResponseRedirect(url)