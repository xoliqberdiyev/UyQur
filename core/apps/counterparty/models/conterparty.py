from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.accounts.models import User


class Counterparty(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=[('active', 'active'), ('inactive', 'inactive')], default='active'
    )
    type = models.CharField(max_length=20, choices=[('supplier', 'supplier')])
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counterparties')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Kontragent'
        verbose_name_plural = 'Kontragentlar'
