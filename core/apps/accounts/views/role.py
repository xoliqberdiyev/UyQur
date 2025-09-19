from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.accounts.models.role import Role
from core.apps.accounts.serializers import role as serializers


class RoleListApiView(generics.ListAPIView):
    serializer_class = serializers.RoleListSerializer
    queryset = Role.objects.all()
    permission_classes = [HasRolePermission]


class RoleCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True, 'message': 'Role created',
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'error': serializer.errors,
            },
            status=400
        )


class RoleUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.RoleSerializer
    queryset = Role.objects.all()
    permission_classes = [HasRolePermission]

    def patch(self, request, id):
        obj = get_object_or_404(Role, id=id)
        serializer = self.serializer_class(data=request.data, instance=obj, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Role updated',
                },
                status=200
            )
        return Response(
            {
                'success': False,
                'error': serializer.errors
            },
            status=400
        )


class RoleDeleteApiView(views.APIView):
    permissions_classes = [HasRolePermission]
    
    def delete(self, request, id):
        obj = get_object_or_404(Role, id=id)
        obj.delete()
        return Response({'success': True, 'message': 'deleted'}, status=204)
    