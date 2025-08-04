from django.contrib import admin 

from core.apps.finance.models.payment_type import PaymentType


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']