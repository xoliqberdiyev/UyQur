from celery import shared_task
from django.db.models import F

from core.apps.wherehouse.models.inventory import Inventory


@shared_task
def create_inventory(wherehouse, quantity, product, unity, price, project_folder, project, unity_price):
      inventory, created = Inventory.objects.get_or_create(
            product_id=product,
            wherehouse_id=wherehouse,
            unity_id=unity,
            defaults=dict(
                  quantity=quantity,
                  price=price,
                  project_folder_id=project_folder,
                  project_id=project,
                  unit_price=unity_price
            )
      )
      if not created:
        inventory.quantity = F('quantity') + quantity
        inventory.save(update_fields=["quantity"])