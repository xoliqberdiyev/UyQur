from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.finance.models import CashTransaction, PaymentType, ExpenceType
from core.apps.counterparty.models import Counterparty
from core.apps.accounts.models import User


class Expence(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expences', null=True)
    cash_transaction = models.ForeignKey(CashTransaction, on_delete=models.CASCADE, related_name='expences')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name='expences')
    project_folder = models.ForeignKey(
        'projects.ProjectFolder', on_delete=models.SET_NULL, related_name='expences', null=True, blank=True
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL, null=True, related_name='expences', blank=True
    )
    expence_type = models.ForeignKey(
        ExpenceType, on_delete=models.SET_NULL, null=True, blank=True, related_name='expences'
    )
    counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, null=True, blank=True, related_name='expences'
    )
    party = models.ForeignKey(
        'orders.Party', on_delete=models.SET_NULL, null=True, blank=True, related_name='expences'
    )

    price = models.PositiveBigIntegerField() 
    exchange_rate = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    currency = models.CharField(
        max_length=3, choices=[('usd','usd'), ('uzs', 'uzs')]
    )
    date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    audit = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='finance/expence/files/')

    def __str__(self):
        return f'{self.cash_transaction} kassa uchun chiqim {self.price}'
    
    class Meta:
        verbose_name = 'chiqim'
        verbose_name_plural = 'chiqimlar'
    
