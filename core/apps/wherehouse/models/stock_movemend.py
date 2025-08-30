from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
# wherehouse
from core.apps.wherehouse.models import WhereHouse, Inventory 
# accounts
from core.apps.accounts.models import User
# projects
from core.apps.projects.models import Project, ProjectFolder


class StockMovemend(BaseModel):
    TYPE = (
        ('EXPECTED', 'kutilmoqda'),
        ('ACCEPTED', 'qabul qilingan'),
        ('CANCELLED', 'bekor qilingan'),
    )

    number = models.IntegerField(default=1)
    wherehouse_to = models.ForeignKey(
        WhereHouse, on_delete=models.CASCADE, related_name='stocks_to'
    )
    wherehouse_from = models.ForeignKey(
        WhereHouse, on_delete=models.CASCADE, related_name='stocks_from'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='stock_movmends', null=True, blank=True
    )
    project_folder = models.ForeignKey(
        ProjectFolder, on_delete=models.SET_NULL, related_name='stock_movmends', null=True, blank=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, related_name='stock_movmends', null=True, blank=True
    )
    movemend_type = models.CharField(max_length=20, choices=TYPE, default='EXPECTED')
    date = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.wherehouse_from} to {self.wherehouse_to}'
    
    class Meta:
        verbose_name = _('Mahsulotlarni kochirish')
        verbose_name_plural = _('Mahsulotlarni kochirish')


class StockMovmendProduct(BaseModel):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name='movemend_products',
        null=True
    )
    quantity = models.PositiveIntegerField()
    stock_movemend = models.ForeignKey(
        StockMovemend, on_delete=models.CASCADE, related_name='movemend_products'
    )

    def __str__(self):
        return str(self.inventory)
    
    class Meta:
        verbose_name = "Ko'chirilgan mahsulot"
        verbose_name_plural = "Ko'chirilgan mahsulotlar"
