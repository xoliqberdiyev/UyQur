from rest_framework import generics
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.accounts.models.role import Role
from core.apps.accounts.serializers import role as serializers


class RoleListApiView(generics.ListAPIView):
    serializer_class = serializers.RoleListSerializer
    queryset = Role.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['settings', 'user']

