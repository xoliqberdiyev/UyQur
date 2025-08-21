from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.orders.models.order import Order
from core.apps.accounts.models import User


class Party(BaseModel):
    orders = models.ManyToManyField(Order, related_name='parties', null=True, blank=True)
    mediator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parties')
    delivery_date = models.DateField()
    payment_date = models.DateField()
    comment = models.TextField(null=True, blank=True)
    audit = models.CharField(
        max_length=20, choices=[('CHECKED', 'tekshirildi'),('PROCESS', 'jarayonda')],
        null=True, blank=True
    )
    audit_comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.mediator.full_name} {self.delivery_date}'
    
    class Meta:
        verbose_name = 'Partiya'
        verbose_name_plural = 'Partiyalar'
