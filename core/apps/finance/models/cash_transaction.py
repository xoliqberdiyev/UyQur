from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.finance.models.payment_type import PaymentType
from core.apps.accounts.models import User


class CashTransactionFolder(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Kassa papkasi'
        verbose_name_plural = 'Kassa papkalari'


class CashTransaction(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    payment_type = models.ManyToManyField(
        PaymentType, related_name='cash_transactions', blank=True
    )
    employees = models.ManyToManyField(User, related_name='cash_transactions')
    status = models.BooleanField(default=False)
    folder = models.ForeignKey(
        CashTransactionFolder, on_delete=models.SET_NULL, related_name='cash_transactions', 
        null=True, blank=True
    )
    total_balance_usd = models.PositiveBigIntegerField(default=0)
    income_balance_usd = models.PositiveBigIntegerField(default=0)
    expence_balance_usd = models.PositiveBigIntegerField(default=0)

    total_balance_uzs = models.PositiveBigIntegerField(default=0)
    income_balance_uzs = models.PositiveBigIntegerField(default=0)
    expence_balance_uzs = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Kassa')
        verbose_name_plural = _('Kassalar')