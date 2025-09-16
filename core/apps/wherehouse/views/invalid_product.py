# django
from django.shortcuts import get_object_or_404
# django filter
from django_filters.rest_framework.backends import DjangoFilterBackend

# rest framework
from rest_framework import generics, parsers, views
from rest_framework.response import Response

# accounts
from core.apps.accounts.permissions.permissions import HasRolePermission
# wherehouse
from core.apps.wherehouse.serializers import invalid_product as serializers
from core.apps.wherehouse.models import InvalidProduct
from core.apps.wherehouse.filters.invalid_product import InvalidProductFilter


class InvalidProductCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.InvalidProductCreateSerializer
    queryset = InvalidProduct.objects.all()
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'invalid product created'},
                status=201
            )
        return Response(
            {'success': True, 'error_message': serializer.errors},
            status=400
        )


class InvalidProductListApiView(generics.GenericAPIView):
    serializer_class = serializers.InvliadProductListSerializer
    queryset = InvalidProduct.objects.select_related(
        'inventory', 'project_folder', 'work'
    ).prefetch_related('witnesses')
    permission_classes = [HasRolePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvalidProductFilter

    def get(self, request):
        invalid_products = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(invalid_products)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(invalid_products, many=True)
        return Response(serializer.data, status=200) 
    

class InvalidProductUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.InvalidProductUpdateSerializer
    queryset = InvalidProduct.objects.all()
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def patch(self, request, id):
        invalid_product = get_object_or_404(InvalidProduct, id=id)
        serializer = self.serializer_class(data=request.data, instance=invalid_product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'updated'},
                status=200
            )
        return Response(
            {'success': False, 'error_message': serializer.errors},
            status=400
        )
    

class InvalidProductDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        invalid_product = get_object_or_404(InvalidProduct, id=id)
        invalid_product.inventory.is_invalid = False
        invalid_product.inventory.quantity += invalid_product.amount
        invalid_product.inventory.save()
        invalid_product.delete()
        return Response(
            {'success': True, 'message': 'invalid product deleted!'},
            status=204
        )
