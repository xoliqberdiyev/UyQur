from rest_framework import generics

from core.apps.projects.models import Builder
from core.apps.projects.serializers import builder as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class BuilderListApiView(generics.ListAPIView):
    serializer_class = serializers.BuilderListSerializer
    queryset = Builder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination



