from django.db import models
from django.utils.translation import gettext_lazy as _

from core.apps.shared.models import BaseModel
from core.apps.projects.models import Project


class ProjectEstimate(BaseModel):
    ...