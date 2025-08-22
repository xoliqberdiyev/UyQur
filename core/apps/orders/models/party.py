from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.orders.models.order import Order
from core.apps.accounts.models import User


class Party(BaseModel):
    number = models.PositiveIntegerField(default=1)
    orders = models.ManyToManyField(Order, related_name='parties', null=True, blank=True)
    mediator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parties')
    # dates
    delivery_date = models.DateField()
    closed_date = models.DateField(null=True, blank=True)
    order_date = models.DateField(auto_now_add=True)
    payment_date = models.DateField()
    
    status = models.CharField(
        max_length=20, choices=[('ORDERED', 'yetkazildi'), ('PROCESS', 'jarayonda')],
        null=True, blank=True
    )
    payment_status = models.FloatField(null=True, blank=True)
    process = models.FloatField(null=True, blank=True)
    confirmation = models.BooleanField(default=False)

    comment = models.TextField(null=True, blank=True)
    audit = models.CharField(
        max_length=20, choices=[('CHECKED', 'tekshirildi'),('PROCESS', 'jarayonda')],
        null=True, blank=True
    )
    audit_comment = models.TextField(null=True, blank=True)
    qqs_price = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    discount = models.PositiveBigIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_party = Party.objects.order_by('number').last()
            if last_party:
                self.number = last_party.number + 1
            else:
                self.number = 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Partiya'
        verbose_name_plural = 'Partiyalar'


class PartyAmount(BaseModel):
    party = models.OneToOneField(Party, on_delete=models.CASCADE, related_name='party_amount')
    total_price = models.PositiveBigIntegerField()
    cost_amount = models.PositiveBigIntegerField(default=0)
    calculated_amount = models.PositiveBigIntegerField(default=0)
    paid_amount = models.PositiveBigIntegerField(default=0)
    payment_amount = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.party} amount'

    class Meta:
        verbose_name = 'Partiya Summasi'
        verbose_name_plural = 'Partiya summalari'
    