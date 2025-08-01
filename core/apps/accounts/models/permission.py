from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class Permission(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name} - {self.code}'
    
    class Meta:
        verbose_name = _('Ruxsatnoma')
        verbose_name_plural = _('Ruxsatnomalar')
