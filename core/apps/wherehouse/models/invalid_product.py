from django.db import models

# shared
from core.apps.shared.models import BaseModel
# wherehouse
from core.apps.wherehouse.models import WhereHouse, Inventory
# projects 
from core.apps.projects.models import ProjectFolder, EstimateWork
# accounts
from core.apps.accounts.models import User


class InvalidProduct(BaseModel):
    INVALID_STATUS = (
        ('BROKEN', 'singan'),
        ('LOST', 'yoqolgan'),
        ('OTHER', 'boshqa'),
    )
    STATUS = (
        ('OPEN', 'ochiq'),
        ('EXPECTED', 'kutilmoqda'),
        ('ACCEPTED', 'qabul qilingan'),
        ('CANCELLED', 'bekor qilingan')
    )

    # relationship
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='invalid_products')
    project_folder = models.ForeignKey(
        ProjectFolder, on_delete=models.CASCADE, related_name='invalid_products'
    )
    witnesses = models.ManyToManyField(User, related_name='invalid_products')
    work = models.ForeignKey(
        EstimateWork, on_delete=models.SET_NULL, null=True, blank=True, related_name='invalid_products'
    )
    wherehouse = models.ForeignKey(WhereHouse, on_delete=models.CASCADE, related_name='invalid_products', null=True)
    # required
    amount = models.PositiveIntegerField()
    invalid_status = models.CharField(max_length=20, choices=INVALID_STATUS, default='other')
    status = models.CharField(max_length=20, choices=STATUS, default='OPEN')
    # optional
    created_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    comment = models.DateField(null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to='invalid_product/files/')

    def __str__(self):
        return f'{self.amount} ta maxsulot yaroqsiz'
    
    class Meta:
        verbose_name = 'yaroqsiz maxsulot'
        verbose_name_plural = 'yaroqsiz maxsulotlar'