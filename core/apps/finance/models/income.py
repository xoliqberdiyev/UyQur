from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.finance.models import CashTransaction, PaymentType, TypeIncome
from core.apps.counterparty.models import Counterparty


class Income(BaseModel):
    cash_transaction = models.ForeignKey(
        CashTransaction, on_delete=models.CASCADE, related_name='incomes'
    )
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, related_name='incomes')
    project_folder = models.ForeignKey(
        'projects.ProjectFolder', on_delete=models.CASCADE, related_name='incomes'
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL, related_name='incomes', null=True, blank=True
    )
    counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, related_name='incomes', null=True, blank=True
    )
    type_income = models.ForeignKey(
        TypeIncome, on_delete=models.SET_NULL, related_name='incomes', null=True, blank=True
    )

    currency = models.CharField(choices=[('uzs', 'uzs'),('usd', 'usd')], max_length=3)
    price = models.PositiveBigIntegerField()
    exchange_rate = models.PositiveBigIntegerField(default=0)
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='finance/income/file/', null=True, blank=True)
    audit = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.cash_transaction} kassa uchun kirim {self.price}'
    
    class Meta:
        verbose_name = 'kirim'
        verbose_name_plural = 'kirimlar'


