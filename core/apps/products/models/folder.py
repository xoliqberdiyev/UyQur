from django.db import models

from core.apps.shared.models import BaseModel


class Folder(BaseModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Papka'
        verbose_name_plural = 'Papkalar'


class SubFolder(BaseModel):
    name = models.CharField(max_length=200)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='sub_folders')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Sub Papka'
        verbose_name_plural = 'Sub Papkalar'

