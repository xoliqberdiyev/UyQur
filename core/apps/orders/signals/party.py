from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from core.apps.orders.models.party import Party, PartyAmount


# @receiver(m2m_changed, sender=Party)
# def change_party_currency(sender, instance, action, **kwargs):
#     currencies = set(instance.orders.values_list("currency", flat=True))
#     print(instance.orders)
#     for order in instance.orders.all():
#         print(order.currency)
#     print(currencies)
#     if "usd" in currencies and "uzs" in currencies:
#         instance.currency = "uzs"
#     elif currencies == {"usd"}:
#         instance.currency = "usd"
#     elif currencies == {"uzs"}:
#         instance.currency = "uzs"
#     instance.save()


# @receiver(post_save, sender=Party)
# def change_party_currency(sender, instance, created, **kwargs):
#     currencies = set()
#     for order in instance.orders.all():
#         currencies.add(order.currency)
#         print(order.currency)
#     if "usd" in currencies and "uzs" in currencies:
#         instance.currency = "uzs"
#     elif currencies == {"usd"}:
#         instance.currency = "usd"
#     elif currencies == {"uzs"}:
#         instance.currency = "uzs"
    
#     instance.save(update_fields=["currency"])
