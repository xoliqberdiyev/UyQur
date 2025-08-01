from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.products.models.product import Product
from core.apps.products.serializers import product as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class ProductListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination