from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel, Region, District
from core.apps.projects.models.builder import Builder
from core.apps.accounts.models.user import User
from core.apps.wherehouse.models.wherehouse import WhereHouse
from core.apps.finance.models.cash_transaction import CashTransaction


class ProjectFolder(BaseModel):
    COLORS = (
        ('ORANGE', 'orange'),
        ('GREEN', 'green'),
        ('BLUE', 'blue'),
        ('PURPLE', 'purple'),
        ('RED', 'red')
    )
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=10, choices=COLORS, default='ORANGE')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Loyiha papkasi')
        verbose_name_plural = _('Loyiha papkalari')


class ProjectLocation(BaseModel):
    address = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='project_locations')
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='project_locations'
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name = _("Loyiha lokatsiyasi")
        verbose_name_plural = _("Loyiha lokatsiyalari")


class Project(BaseModel):
    STATUS = (
        ('PLANNED', 'planned'),
        ('IN_PROGRESS', 'in progress'),
        ('FINISHED', 'finished'),
        ('SUSPENDED', 'suspended'),
    )

    name = models.CharField(max_length=200)
    location = models.ForeignKey(
        ProjectLocation, on_delete=models.SET_NULL, null=True, related_name='projects'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    folder = models.ForeignKey(
        ProjectFolder, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects'
    )
    builder = models.ForeignKey(
        Builder, on_delete=models.CASCADE, related_name='projects', null=True
    )
    area = models.PositiveBigIntegerField(null=True)

    # project workers
    boss = models.ManyToManyField(User, related_name='project_bosses')
    foreman = models.ManyToManyField(User, related_name='project_foremans')
    other_members = models.ManyToManyField(User, related_name='project_members')

    # project settings
    wherehouse = models.ManyToManyField(
        WhereHouse, related_name='projects'
    )
    cash_transaction = models.ManyToManyField(
        CashTransaction, related_name='projects'
    )
    currency = models.CharField(choices=[('usd', 'usd'),('uzs','uzs')], max_length=3, default='uzs')
    benifit_plan = models.PositiveBigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='PLANNED')
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Loyiha')
        verbose_name_plural = _('Loyihalar')