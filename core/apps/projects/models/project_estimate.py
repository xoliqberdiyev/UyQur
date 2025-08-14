from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.projects.models import Project
from core.apps.products.models import Unity, Product
from core.apps.accounts.models import User


class ProjectEstimate(BaseModel):
    number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.number}.{self.name}'
    
    class Meta:
        verbose_name = _('Loyiha smetasi')
        verbose_name_plural = _('Loyiha smetalari')


class EstimateWork(BaseModel):
    STATUS = (
        ('OPEN', 'ochiq'),
        ('IN_PROGRESS', 'bajarilmoqda'),
        ('DONE', 'bajarildi'),
    )

    number = models.PositiveIntegerField(default=1)
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unity = models.ForeignKey(
        Unity, on_delete=models.SET_NULL, null=True, related_name='estimate_works'
    )
    price = models.PositiveBigIntegerField(null=True, blank=True)
    estimate = models.ForeignKey(
        ProjectEstimate, on_delete=models.CASCADE, related_name='estimate_works'
    )
    date = models.DateField(null=True, blank=True)
    total_price = models.PositiveBigIntegerField(default=0)

    status = models.CharField(choices=STATUS, max_length=20, default='ochiq')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    employee = models.ManyToManyField(User, related_name='estimate_work', blank=True)
    percentage = models.PositiveSmallIntegerField(db_default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.number}.{self.name}"
    
    class Meta:
        verbose_name = _("Smeta ish")
        verbose_name = _("Smeta ishlar")


class EstimateProduct(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='estimate_products')
    quantity = models.PositiveIntegerField(default=1)
    unity = models.ForeignKey(
        Unity, on_delete=models.SET_NULL, null=True, related_name='estimate_products'
    )
    price = models.PositiveBigIntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    estimate_work = models.ForeignKey(EstimateWork, on_delete=models.CASCADE, related_name='estimate_products', null=True)

    def __str__(self):
        return f'{self.product} - {self.price}'
    
    class Meta:
        verbose_name = _('Smeta mahsuloti')
        verbose_name_plural = _('Smeta mahsulotlari')