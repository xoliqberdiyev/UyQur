from celery import shared_task

from core.apps.wherehouse.models.inventory import Inventory


@shared_task
def create_inventory(wherehouse, quantity, product, unity, price):
    Inventory.objects.create(
         wherehouse_id=wherehouse,
         quantity=quantity,
         product_id=product,
         unity_id=unity,
         price=price
    )
