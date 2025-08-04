from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.projects.models.builder import Builder
from core.apps.accounts.models.user import User
from core.apps.wherehouse.models.wherehouse import WhereHouse
from core.apps.finance.models import CashTransaction


class ProjectFolder(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Loyiha papkasi')
        verbose_name_plural = _('Loyiha papkalari')


class Project(BaseModel):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
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
    wherehouse = models.ForeignKey(
        WhereHouse, on_delete=models.CASCADE, related_name='projects', null=True
    )
    cash_transaction = models.ForeignKey(
        CashTransaction, on_delete=models.CASCADE, related_name='projects', null=True
    )
    currency = models.CharField(choices=[('usd', 'usd'),('uzs','uzs')], max_length=3, default='uzs')
    benifit_plan = models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Loyiha')
        verbose_name_plural = _('Loyihalar')