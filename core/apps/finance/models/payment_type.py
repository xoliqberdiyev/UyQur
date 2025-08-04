from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class PaymentType(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("To'lov turi")
        verbose_name_plural = _("To'lov turlari")
            