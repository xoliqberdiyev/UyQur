from django.db import models

from core.apps.shared.models import BaseModel
from core.apps.accounts.models import User
from core.apps.finance.models import ExpenceType
from core.apps.counterparty.models import Counterparty


class ExpenceContract(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expence_contracts')
    project_folder = models.ForeignKey(
        'projects.ProjectFolder', on_delete=models.CASCADE, related_name='expence_contracts'
    )
    project = models.ForeignKey(
        'projects.Project', on_delete=models.SET_NULL, related_name='expence_contracts', null=True, blank=True
    )
    expence_type = models.ForeignKey(
        ExpenceType, on_delete=models.SET_NULL, related_name='expence_contracts', null=True, blank=True
    )
    counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, related_name='expence_contracts', null=True, blank=True
    )

    price = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3, choices=[('uzs', 'uzs'), ('usd', 'usd')])
    date = models.DateField()
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.counterparty} chiqim shartnomasa: {self.price} {self.currency}'
    
    class Meta:
        verbose_name = 'Chiqim Shartnomasi'
        verbose_name_plural = 'Chiqim Shartnomalari'