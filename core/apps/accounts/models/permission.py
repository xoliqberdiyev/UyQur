from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel


class PermissionToAction(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Harakatlar uchun ruxsatnoma')
        verbose_name_plural = _('Harakatlar uchun ruxsatnomalar')


class PermissionToTab(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    permission_to_actions = models.ManyToManyField(
        PermissionToAction, related_name='permission_to_tabs'
    )

    def __str__(self):
        return f'{self.name} - {self.code}'
    
    class Meta:
        verbose_name = _("Bo'lim uchun ruxsatnoma")
        verbose_name_plural = _("Bo'lim uchun ruxsatnomalar")


class Permission(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    permission_tab = models.ManyToManyField(PermissionToTab, related_name='permissions')

    def __str__(self):
        return f'{self.name} - {self.code}'
    
    class Meta:
        verbose_name = _('Sahifa uchun ruxsatnoma')
        verbose_name_plural = _('Sahifa uchun ruxsatnomalar')