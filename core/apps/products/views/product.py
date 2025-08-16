from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.products.models import Product
from core.apps.products.serializers import product as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class ProductListApiView(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.select_related('unity').only(
        'id', 'name', 'type', 'unity'
    )
    permission_classes = [HasRolePermission]
    required_permissions = ['product']
    pagination_class = CustomPageNumberPagination


class ProductCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product']
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': "product successfully created!"},
                status=201
            )
        return Response(
            {
                "success": False,
                "message": "an error occurred while adding th product.",
                "error": serializer.errors
            },
            status=400
        )


class ProductUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProductUpdateSerializer
    queryset = Product.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product']

    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(data=request.data, instance=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'product successfully updated!'},
                status=200
            )
        return Response(
            {
                'success': False,
                'message': "an error occurred while updating the product.",
                "error": serializer.errors,
            },
            status=400
        )

    def patch(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = self.serializer_class(data=request.data, instance=product, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, "message": "product successfully updated!"},
                status=200
            )
        return Response(
            {
                "successs": False,
                "message": "an error accurred while updating the product.",
                "error": serializer.errors
            },
            status=400
        )


class ProductDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['product']

    def delete(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return Response(
            {'success': True, 'message': 'product successfully deleted!'}, 
            status=204
        )