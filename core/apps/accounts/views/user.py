from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.models import User
from core.apps.accounts.serializers import user as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.accounts.utils.permission import get_permissions_with_tabs


class UserProfileApiView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response({
            "success": True,
            'user_data': serializer.data,
            'permissions_to_page': get_permissions_with_tabs(user)
        }, status=200)
    

class UserProfileUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data, instance=user, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'updated'}, status=200)
        return Response({"success": False, "message": serializer.errors}, status=400)


class UserDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['delete_user']

    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response(status=204)