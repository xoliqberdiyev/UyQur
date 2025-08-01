from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.products.models import Unity
from core.apps.products.serializers import unity as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class UnityListApiView(generics.ListAPIView):
    serializer_class = serializers.UnityListSerializer
    queryset = Unity.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []