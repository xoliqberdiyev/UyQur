from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.company.models.branch import Branch


class WhereHouse(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='wherehouses')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('omborxona')
        verbose_name_plural = _('omborxonalar')