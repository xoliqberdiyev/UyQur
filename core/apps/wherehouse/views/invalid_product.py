from rest_framework import generics, parsers
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.wherehouse.serializers import invalid_product as serializers
from core.apps.wherehouse.models import InvalidProduct


class InvalidProductCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.InvalidProductCreateSerializer
    queryset = InvalidProduct.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []
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
    required_permissions = []

    def get(self, request):
        invalid_products = self.queryset
        page = self.paginate_queryset(invalid_products)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(invalid_products, many=True)
        return Response(serializer.data, status=200) 