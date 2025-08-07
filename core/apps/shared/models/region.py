from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class Region(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Mintaqa")
        verbose_name_plural = _("Mintaqalar")


class District(BaseModel):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Tuman")
        verbose_name_plural = _("Tumanlar")