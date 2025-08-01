from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.wherehouse.models.wherehouse import WhereHouse
from core.apps.products.models.product import Product


class StockMovemend(BaseModel):
    TYPE = (
        ('IN', 'in'),
        ('OUT', 'out'),
        ('TRANSFER', 'transfer'),
    )

    wherehouse_to = models.ForeignKey(
        WhereHouse, on_delete=models.CASCADE, related_name='stocks_to'
    )
    wherehouse_from = models.ForeignKey(
        WhereHouse, on_delete=models.CASCADE, related_name='stocks_from'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='stocks'
    )
    quantity = models.PositiveIntegerField(default=0)
    movemend_type = models.CharField(max_length=20, choices=TYPE)

    def __str__(self):
        return f'{self.product} send from {self.wherehouse_from} to {self.wherehouse_to}'
    
    class Meta:
        verbose_name = _('Mahsulotlarni kochirish')
        verbose_name_plural = _('Mahsulotlarni kochirish')
