from django.shortcuts import get_object_or_404

from rest_framework import generics, views, filters
from rest_framework.response import Response

from django_filters.rest_framework.backends import DjangoFilterBackend

from core.apps.wherehouse.serializers import inventory as serializers
from core.apps.wherehouse.models import WhereHouse, Inventory
from core.apps.accounts.permissions.permissions import HasRolePermission


class InventoryListApiView(generics.GenericAPIView):
    serializer_class = serializers.InventoryListSerializer
    queryset = Inventory.objects.select_related('product', 'unity').exclude(is_invalid=True)
    permissions_classes = [HasRolePermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        'product__name', 'unity__value'
    ]

    def get(self, request):
        wherehouse_ids = request.query_params.getlist('wherehouse_id')
        project_folder_ids = request.query_params.getlist('project_folder_id')
        project_ids = request.query_params.getlist('project_ids')
        product_exists = request.query_params.get('product_exist')
        inventories = self.filter_queryset(self.queryset)

        if wherehouse_ids:
            inventories = inventories.filter(wherehouse__in=wherehouse_ids)
        if project_folder_ids:
            inventories = inventories.filter(project_folder__in=project_folder_ids)
        if project_ids:
            inventories = inventories.filter(project__in=project_ids)
        if product_exists == 'true':
            inventories = inventories.exclude(quantity=0)
        elif product_exists == 'false':
            inventories = inventories.filter(quantity=0) 
        page = self.paginate_queryset(inventories)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(inventories, many=True)
        return Response(serializer.data, status=200)
