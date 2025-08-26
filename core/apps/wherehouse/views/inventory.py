from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.wherehouse.serializers import inventory as serializers
from core.apps.wherehouse.models import WhereHouse, Inventory
from core.apps.accounts.permissions.permissions import HasRolePermission


class InventoryListApiView(generics.GenericAPIView):
    serializer_class = serializers.InventoryListSerializer
    queryset = Inventory.objects.all()
    permissions_class = [HasRolePermission]
    required_permissions = ['wherehouse']

    def get(self, request):
        wherehouse_ids = request.query_params.getlist('wherehouse_id')
        if wherehouse_ids:
            inventories = Inventory.objects.filter(wherehouse__in=wherehouse_ids)
        else:
            inventories = Inventory.objects.all()
        page = self.paginate_queryset(inventories)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(inventories, many=True)
        return Response(serializer.data, status=200)
