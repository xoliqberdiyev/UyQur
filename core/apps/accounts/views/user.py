from django.shortcuts import get_object_or_404

from rest_framework import generics, views, parsers
from rest_framework.response import Response

from core.apps.accounts.models import User
from core.apps.accounts.serializers import user as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.accounts.utils.permission import get_permissions_with_tabs
from core.apps.shared.paginations.custom import CustomPageNumberPagination
from core.apps.accounts.serializers.permission import PermissionListSerializer
from core.apps.accounts.models.permission import Permission


class UserProfileApiView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [HasRolePermission]

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({
            "success": True,
            'user_data': serializer.data,
            # 'permissions_to_page': get_permissions_with_tabs(user)
        }, status=200)
    

class UserProfileUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'updated'}, status=200)
        return Response({"success": False, "message": serializer.errors}, status=400)


class UserDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['settings', 'user']

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response(status=204)
    

class UserCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, 'message': 'created'},
                status=201
            )
        return Response(
            {'success': False, 'message': serializer.errors},
            status=400
        )
    

class UserListApiView(generics.ListAPIView):
    serializer_class = serializers.UserListSerializer
    queryset = User.objects.select_related('role')
    permission_classes = [HasRolePermission]
    pagination_class = CustomPageNumberPagination


class UserUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = self.serializer_class(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'updated'}, status=200)
        return Response({"success": False, "message": serializer.errors}, status=400)


class UserPermissionListApiView(generics.GenericAPIView):
    serializer_class = PermissionListSerializer
    queryset = None
    permission_classes = [HasRolePermission]

    def get(self, request):
        user = request.user

        if not user.role:
            return Response({'success': False, 'message': 'User has no role assigned'}, status=400)

        serializer = self.serializer_class(user.role.permissions, many=True)
        return Response(
            {'success': True, 'permissions': serializer.data},
            status=200
        )