from django.db import models

from core.apps.shared.models import BaseModel


class TypeIncome(BaseModel):
    name = models.CharField(max_length=200)
    category = models.CharField(
        choices=[('OTHERS', 'boshqalar'), ('CONTANT_INCOME', 'doimiy daromad')], max_length=20
    )
    activity = models.CharField(
        max_length=20, choices=[('FINANCIAL', 'moliyaviy'), ('CAPITAL', 'sarmoya')]
    )
    comment = models.CharField(max_length=200)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Daromad turi'
        verbose_name = 'Daromad turlari'
    