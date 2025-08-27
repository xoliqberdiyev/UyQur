from django.db import models
from django.utils.translation import gettext_lazy as _

# shared
from core.apps.shared.models import BaseModel
# warehouse
from core.apps.wherehouse.models.wherehouse import WhereHouse
# products
from core.apps.products.models.product import Product
from core.apps.products.models.unity import Unity
# projects
from core.apps.projects.models import Project, ProjectFolder


class Inventory(BaseModel):
    wherehouse = models.ForeignKey(WhereHouse, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    unity = models.ForeignKey(Unity, on_delete=models.SET_NULL, related_name='inventories', null=True)
    price = models.PositiveBigIntegerField(default=0)
    project_folder = models.ForeignKey(
        ProjectFolder, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='inventories'
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='inventories'
    )
    is_invalid = models.BooleanField(default=False)
    unit_price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'{self.product} in {self.wherehouse}'

    class Meta:
        verbose_name = _('inventar')
        verbose_name_plural = _("inventarlar")
        