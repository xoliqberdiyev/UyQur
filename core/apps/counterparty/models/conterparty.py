from django.db import models

from core.apps.shared.models import BaseModel, Region, District
from core.apps.accounts.models import User


class CounterpartyFolder(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Kontragent papkasi'
        verbose_name_plural = 'Kontragent papkalari'


class Counterparty(BaseModel):
    TYPE = (
        ('SUPPLIER', "ta'minotchi"),
        ('WORKER', 'ishchi')
    )

    inn = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True)
    
    type = models.CharField(max_length=20, choices=TYPE, default='SUPPLIER')
    folder = models.ForeignKey(
        CounterpartyFolder, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='counterparties',
    )
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='counterparties'
    )
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True, related_name='counterparties'
    )
    balance = models.PositiveBigIntegerField(null=True, blank=True)
    balance_currency = models.CharField(
        max_length=3, choices=[('usd', 'usd'), ('uzs', 'uzs')], null=True, blank=True
    )
    balance_date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Kontragent'
        verbose_name_plural = 'Kontragentlar'
