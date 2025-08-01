from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class Product(BaseModel):
    TYPE = (
        ("TANGIBLE", "ushlab bo'ladigan"),
        ("INTANGIBLE", "ushlab bo'lmaydigan"),
    )

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE, default="TANGIBLE")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Mahsulot')
        verbose_name_plural = _("Mahsulotlar")