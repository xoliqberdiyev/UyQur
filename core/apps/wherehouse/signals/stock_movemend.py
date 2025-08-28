from django.dispatch import receiver
from django.db.models.signals import post_save

from core.apps.wherehouse.models import StockMovemend

@receiver(post_save, sender=StockMovemend)
def set_stock_movemend_number(sender, instance, created, **kwargs):
    if created:
        last_party = StockMovemend.objects.order_by('number').last()
        instance.number = (last_party.number + 1) if last_party else 1
        instance.save(update_fields=["number"])