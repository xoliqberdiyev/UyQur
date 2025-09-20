from rest_framework import generics
from rest_framework.response import Response

from core.apps.accounts.serializers import permission as serializers
from core.apps.accounts.models.permission import Permission, PermissionToAction, PermissionToTab
from core.apps.accounts.permissions.permissions import HasRolePermission


class PermissionListApiView(generics.ListAPIView):
    serializer_class = serializers.PermissionListSerializer
    queryset = None
    permission_classes = [HasRolePermission]

    def get(self, request):
        permissions = Permission.objects.all()
        permission_to_tabs = PermissionToTab.objects.all()
        permission_to_actions = PermissionToAction.objects.all()
        serializer = self.serializer_class(permissions, many=True)
        tab_permissions = serializers.PermissionToTabListSerializer(permission_to_tabs, many=True)
        action_permissions = serializers.PermissionToActionListSerializer(permission_to_actions, many=True)
        return Response(
            {
                'success': True,
                'permissions': serializer.data,
                'tab_permissions': tab_permissions.data,
                'action_permissions': action_permissions.data
            },
            status=200
        )