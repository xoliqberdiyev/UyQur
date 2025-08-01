from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.company.models.comany import Company


class Branch(BaseModel):
    name = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    location = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name} - {self.company}"
    
    class Meta:
        verbose_name = _('Filial')
        verbose_name_plural = _('Filialar')
