from django.db import models

from core.apps.shared.models import BaseModel


class UsdCourse(BaseModel):
    value = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = 'dollar kursi'
        verbose_name_plural = 'dollar kursi'

