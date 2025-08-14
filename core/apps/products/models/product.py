from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class Product(BaseModel):
    TYPE = (
        ("MECHANISM", "maxanizm"),
        ("PRODUCT", "product"),
        ("HUMAN_RESOURCE", "inson resursi"),
        ("SERVICE", 'xizmat')
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE, default="TANGIBLE")
    unity = models.ForeignKey(
        'products.Unity', on_delete=models.SET_NULL, related_name='products', null=True
    )
    product_code = models.CharField(max_length=200, null=True, blank=True)
    folder = models.ForeignKey(
        'products.Folder', on_delete=models.CASCADE, related_name='products', null=True
    )
    sub_folder = models.ForeignKey(
        'products.SubFolder', on_delete=models.SET_NULL, related_name='products', null=True, blank=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Mahsulot')
        verbose_name_plural = _("Mahsulotlar")