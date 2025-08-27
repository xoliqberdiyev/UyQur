from celery import shared_task

from core.apps.wherehouse.models.inventory import Inventory


@shared_task
def create_inventory(wherehouse, quantity, product, unity, price, project_folder, project, unity_price):
      Inventory.objects.create(
            wherehouse_id=wherehouse,
            quantity=quantity,
            product_id=product,
            unity_id=unity,
            price=price,
            project_folder_id=project_folder,
            project_id=project,
            unit_price=unity_price
      )
