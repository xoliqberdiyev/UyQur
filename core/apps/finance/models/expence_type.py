from django.db import models

from core.apps.shared.models import BaseModel


class ExpenceType(BaseModel):
    name = models.CharField(max_length=200)
    category = models.CharField(
        choices=[('OTHERS', 'boshqalar'), ('FIXED_COST', 'doimiy xarajat')], max_length=20
    )
    activity = models.CharField(
        max_length=20, choices=[('FINANCIAL', 'moliyaviy'), ('CAPITAL', 'sarmoya')]
    )
    comment = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'xarajat turi'
        verbose_name_plural = 'xarajat turlari'
