from django.shortcuts import get_object_or_404

from rest_framework import generics, parsers, filters
from rest_framework.response import Response

# django-filter
from django_filters.rest_framework.backends import DjangoFilterBackend

# warehouse
from core.apps.wherehouse.serializers import stock_movmend as serializers
from core.apps.wherehouse.models import StockMovemend, StockMovmendProduct
from core.apps.wherehouse.filters.stock_movemend import StockMovemendFilter
# accounts
from core.apps.accounts.permissions.permissions import HasRolePermission


class StockMovemendCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.StockMovmendCreateSerializer
    queryset = StockMovemend.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'stock movemend created'},
                status=200
            )
        return Response(
            {'success': True, 'error_message': serializer.errors}
        )


class StockMovemendListApiView(generics.GenericAPIView):
    serializer_class = serializers.StockMovemendListSerializer
    queryset = StockMovemend.objects.select_related(
        'wherehouse_to', 'wherehouse_from', 'recipient', 'project_folder', 'project'
    ).prefetch_related('movmend_products')
    permission_classes = [HasRolePermission]
    required_permissions = []
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = StockMovemendFilter
    search_fields = [
        'number', 'wherehouse_to__name', 'wherehouse_from__name', 'project_folder__name',
        'project__name', 'movemend_type', 'date', 'comment'
    ]

    def get(self, request):
        queryset = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=200)
    

class StockMovemendDeleteApiView(generics.GenericAPIView):
    serializer_class = None
    permission_classes = [HasRolePermission]
    required_permissions = []
    queryset = StockMovemend.objects.all()

    def delete(self, request, id):
        stock_movemend = get_object_or_404(StockMovemend, id=id)
        if stock_movemend.movemend_type == 'EXPECTED' or stock_movemend.movemend_type == 'CANCELLED':
            stock_movemend.delete()        
            return Response(
                {'success': True, 'message': 'stock movemend deleted'}, 
                status=204
            )
        else:
            return Response(
                {'success': False, 'message': 'can not delete stock movemend'},
                status=400
            )


class StockMovemendProductRemoveApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    required_permissions = []
    queryset = StockMovmendProduct.objects.all()
    serializer_class = None

    def delete(self, request, stock_movemend_id, stock_movemend_product_id):
        stock_movemend = get_object_or_404(StockMovemend, id=stock_movemend_id)
        stock_movemend_product = stock_movemend.movmend_products.filter(id=stock_movemend_product_id).first()
        if not stock_movemend_product:
            return Response(
                {
                    'success': False,
                    'message': 'Product Does not belong to the stock_movemend',
                },
                status=404
            )
        stock_movemend.movmend_products.remove(stock_movemend_product)
        return Response(
            {'success': True, 'message': 'removed'},
            status=200
        )
