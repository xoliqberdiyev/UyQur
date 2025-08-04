from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.finance.models.payment_type import PaymentType
from core.apps.accounts.models import User


class CashTransaction(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    payment_type = models.ForeignKey(
        PaymentType, on_delete=models.CASCADE, related_name='cash_transactions', null=True
    )
    employees = models.ManyToManyField(User, related_name='cash_transactions')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Kassa')
        verbose_name_plural = _('Kassalar')