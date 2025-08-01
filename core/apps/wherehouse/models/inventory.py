from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.wherehouse.models.wherehouse import WhereHouse
from core.apps.products.models.product import Product


class Inventory(BaseModel):
    wherehouse = models.ForeignKey(WhereHouse, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')

    def __str__(self):
        return f'{self.product} in {self.wherehouse}'

    class Meta:
        verbose_name = _('inventar')
        verbose_name_plural = _("inventarlar")
        