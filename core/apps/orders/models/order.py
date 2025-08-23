from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.products.models import Product, Unity
from core.apps.projects.models import Project, ProjectFolder
from core.apps.accounts.models import User
from core.apps.wherehouse.models import WhereHouse
from core.apps.counterparty.models import Counterparty


class Order(BaseModel):
    STATUS = (
        ('NEW', 'yangi'),
        ('CANCELLED', "bekor qilindi"),
        ('ACCEPTED', 'qabul qilindi'),
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orders'
    )
    unity = models.ForeignKey(
        Unity, on_delete=models.CASCADE, related_name='orders'
    )
    project_folder = models.ForeignKey(
        ProjectFolder, on_delete=models.SET_NULL, related_name='order', null=True, blank=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, related_name='orders', null=True, blank=True
    )
    wherehouse = models.ForeignKey(
        WhereHouse, on_delete=models.CASCADE, related_name='orders'
    )
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True)
    counterparty = models.ForeignKey(
        Counterparty, on_delete=models.SET_NULL, null=True, blank=True, related_name='order'
    )
    
    date = models.DateField(null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS, default="NEW")
    unit_amount = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    currency = models.CharField(
        choices=[('uzs', 'uzs'), ('usd', 'usd')], default='uzs', null=True, blank=True, max_length=3
    )
    total_price = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    qqs_price = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    amount = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    qqs = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return f"{self.product} {self.unity} quantity order"
    
    class Meta:
        verbose_name = _("Buyurtma")
        verbose_name_plural = _("Buyurtmalar")