from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.orders.models import Order
from core.apps.counterparty.models import Counterparty


class Offer(BaseModel):
    PRICE_TYPE = (
        ('UZS', 'uzs'),
        ('USD', 'usd')
    )
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='offers')
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE, related_name='offers', null=True)
    price = models.PositiveBigIntegerField()
    price_type = models.CharField(choices=PRICE_TYPE, default='uzs')
    phone = models.CharField(max_length=15, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    qqs = models.BooleanField(default=False, null=True, blank=True)
    number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_offer = Offer.objects.filter(order=self.order).order_by('-number').first()
            if last_offer:
                self.number = last_offer.number + 1
            else:
                self.number = 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Taklif'
        verbose_name_plural = 'Takliflar'
        