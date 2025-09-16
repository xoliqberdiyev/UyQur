from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.projects.serializers import estimate_product as serializers
from core.apps.projects.models.project_estimate import EstimateProduct
from core.apps.accounts.permissions.permissions import HasRolePermission


class EstimateProductCreateApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    serializer_class = serializers.EstimateProductCreateSerializer
    queryset = EstimateProduct.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, 'message': 'created'}, status=201)
        return Response({'success': False, 'message': serializer.errors}, status=400)


class EstimateProductUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.EstimateProductUpdateSerializer
    queryset = EstimateProduct.objects.all()
    permission_classes = [HasRolePermission]

    def patch(self, request, id):
        estimate_product = get_object_or_404(EstimateProduct, id=id)
        serializer = self.serializer_class(data=request.data, instance=estimate_product, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": 'updated'}, status=200)
        return Response({"success": False, 'message': serializer.errors}, status=400)
    

class EstimateProductDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        estimate_product = get_object_or_404(EstimateProduct, id=id)
        estimate_product.delete()
        return Response({"success": True}, status=204)
