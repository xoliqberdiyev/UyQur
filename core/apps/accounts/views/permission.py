from rest_framework import generics
from rest_framework.response import Response

from core.apps.accounts.serializers import permission as serializers
from core.apps.accounts.models.permission import Permission
from core.apps.accounts.permissions.permissions import HasRolePermission


class PermissionListApiView(generics.ListAPIView):
    queryset = Permission.objects.prefetch_related('permission_tab')
    serializer_class = serializers.PermissionListSerializer
    permission_classes = [HasRolePermission]
    required_permissions = ['settings', 'permissions', 'role']
