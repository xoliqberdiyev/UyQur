from django.shortcuts import get_object_or_404

from rest_framework import generics, views, status
from rest_framework.response import Response

from core.apps.finance.models import TypeIncome
from core.apps.finance.serializers.type_income import TypeIncomeSerializer
from core.apps.accounts.permissions.permissions import HasRolePermission


class TypeIncomeCreateApiView(generics.GenericAPIView):
    serializer_class = TypeIncomeSerializer
    queryset = TypeIncome.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True, 
                    'message': 'Type income created'
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'Type income not created',
                'error': serializer.errors,
            },
            status=400
        )
    

class TypeIncomeListApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    queryset = TypeIncome.objects.all()
    serializer_class = TypeIncomeSerializer
    
    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            ser = self.serializer_class(page, many=True)
            return self.get_paginated_response(ser.data)
        
    
class TypeIncomeUpdateApiView(generics.GenericAPIView):
    serializer_class = TypeIncomeSerializer
    queryset = TypeIncome.objects.all()
    permission_classes = [HasRolePermission]

    def patch(self, request, id):
        obj = get_object_or_404(TypeIncome, id=id)
        ser = self.serializer_class(data=request.data, instance=obj, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(
                {
                    'success': True,
                    'message': 'updated'
                },
                status=200
            )
        return Response(
            {
                'success': False,
                'message': 'error',
                'error': ser.errors,
            },
            status=400
        )


class TypeIncomeDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        obj = get_object_or_404(TypeIncome, id=id)
        obj.delete()
        return Response(
            {'success': True, 'message': 'deleted'}, status=204
        )
