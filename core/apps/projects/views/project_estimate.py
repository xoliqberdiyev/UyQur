from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.projects.models.project_estimate import ProjectEstimate, EstimateProduct, EstimateWork
