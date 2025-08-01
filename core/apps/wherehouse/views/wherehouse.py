from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.wherehouse.models import WhereHouse, Inventory
from core.apps.wherehouse.serializers import wherehouse as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class WhereHouseListApiView(generics.ListAPIView):
    serializer_class = serializers.WhereHouseListSerializer
    queryset = WhereHouse.objects.select_related('branch')
    permission_classes = [HasRolePermission]
    required_permissions = []


class WhereHouseDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.WhereHouseDetailSerializer
    queryset = WhereHouse.objects.select_related('branch').prefetch_related('inventories')
    permission_classes = [HasRolePermission]
    required_permissions = []
    lookup_field = 'id'
