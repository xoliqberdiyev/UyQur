from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class Project(BaseModel):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Loyiha')
        verbose_name_plural = _('Loyihalar')


class ProjectDepartment(BaseModel):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_departments'
    )
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Loyiha Bo'limi")
        verbose_name_plural = _("Loyiha Bo'limlari")