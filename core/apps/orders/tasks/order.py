from celery import shared_task

from core.apps.wherehouse.models.inventory import Inventory


@shared_task
def create_inventory(wherehouse, quantity, product, unity, price):
    Inventory.objects.create(
        wherehouse__id=wherehouse,
        quantity=quantity,
        product__id=product,
        unity__id=unity,
        price=price
    )
