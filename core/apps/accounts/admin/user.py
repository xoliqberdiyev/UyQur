from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from core.apps.accounts.models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": (
            "full_name", 'phone_number', "role", 'profile_image', 'is_blocked'
        )}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "username", "phone_number", "full_name", "is_blocked", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_blocked")
    search_fields = ("username", "full_name", "phone_number")
    ordering = ("username",)