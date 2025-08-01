from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class Unity(BaseModel):
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.value
    
    class Meta:
        verbose_name = _('Birlik')
        verbose_name_plural = _("Birliklar")