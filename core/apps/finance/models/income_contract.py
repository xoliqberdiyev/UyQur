from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.finance.models import TypeIncome
from core.apps.counterparty.models import Counterparty
from core.apps.accounts.models import User


class IncomeContract(BaseModel):
    project_folder = models.ForeignKey(
        'projects.ProjectFolder', on_delete=models.CASCADE, related_name='income_contracts'
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL, related_name='income_contracts', null=True
    )
    income_type = models.ForeignKey(
        TypeIncome, on_delete=models.SET_NULL, related_name='income_contracts', null=True
    )
    counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, related_name='income_contracts', null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income_contracts')

    price = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3, choices=[('uzs', 'uzs'), ('usd', 'usd')])
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.counterparty} kirim shartnomasa: {self.price} {self.currency}'
    
    class Meta:
        verbose_name = 'Kirim Shartnomasi'
        verbose_name_plural = 'Kirim Shartnomalari'