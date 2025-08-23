from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.orders.models import Party


@receiver(post_save, sender=Party)
def set_party_number(sender, instance, created, **kwargs):
    if created:
        last_party = Party.objects.order_by('number').last()
        instance.number = (last_party.number + 1) if last_party else 1
        instance.save(update_fields=["number"])