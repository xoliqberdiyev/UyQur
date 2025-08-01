from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.accounts.models.permission import Permission


class Role(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Rol')
        verbose_name_plural = _('Rollar')