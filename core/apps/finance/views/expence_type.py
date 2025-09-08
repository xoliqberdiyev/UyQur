from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.finance.models import ExpenceType
from core.apps.finance.serializers.expence_type import ExpenceTypeSerializer


class ExpenceTypeCreateApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    serializer_class = ExpenceTypeSerializer
    queryset = ExpenceType.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'expence type created'                    
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'expence type create failed',
                'error': serializer.errors,
            },
            status=400
        )


class ExpenceTypeListApiView(generics.GenericAPIView):
    serializer_class = ExpenceTypeSerializer
    queryset = ExpenceType.objects.all()
    permission_classes = [HasRolePermission]

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class ExpenceTypeUpdateApiView(generics.GenericAPIView):
    serializer_class = ExpenceTypeSerializer
    queryset = ExpenceType.objects.all()
    permission_classes = [HasRolePermission]

    def patch(self, request, id):
        obj = get_object_or_404(ExpenceType, id=id)
        serializer = self.serializer_class(data=request.data, instance=obj, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'expence type updated'
                },
                status=200
            )
        return Response(
            {
                'success': False,
                'message': 'expence type update failed',
                'error': serializer.errors
            },
            status=400
        )
    

class ExpenceTypeDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        obj = get_object_or_404(ExpenceType, id=id)
        obj.delete()
        return Response(
            {'success': True, 'message': 'deleted'}, status=204
        )