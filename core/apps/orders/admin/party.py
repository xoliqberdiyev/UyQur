from django.contrib import admin

from core.apps.orders.models import Party, PartyAmount, DeletedParty


class PartyAmountInline(admin.StackedInline):
    model = PartyAmount
    extra = 1
    show_change_link = True


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['id','number','mediator', 'delivery_date', 'payment_date', 'is_deleted']
    inlines = [PartyAmountInline]    


@admin.register(PartyAmount)
class PartyAmountAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_price', 'cost_amount']

    def has_module_permission(self, request):
        return False

@admin.register(DeletedParty)
class DeletedPartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'deleted_date', 'party']