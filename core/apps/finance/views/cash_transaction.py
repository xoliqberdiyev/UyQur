from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.finance.models import CashTransaction
from core.apps.finance.serializers import cash_transaction as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class CashTransactionListApiView(generics.ListAPIView):
    permission_classes = [HasRolePermission]
    required_permissions = []
    serializer_class = serializers.CashTransactionListSerializer
    queryset = CashTransaction.objects.select_related('payment_type').prefetch_related('employees')
    pagination_class = CustomPageNumberPagination


class CashTransactionCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.CashTransactionCreateSerializer
    queryset = CashTransaction.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project', 'project_folder']


class CashTransactionUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.CashTransactionUpdateSerializer
    queryset = CashTransaction.objects.all()
    permission_classes = [HasRolePermission]

    def patch(self, request, id):
        obj = get_object_or_404(CashTransaction, id=id)
        ser = self.serializer_class(data=request.data, instance=obj, partial=True)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(
                {
                    'success': True,
                    'message': 'Cash Transaction successfully updated!'
                },
                status=200,
            )
        return Response(
            {
                'success': False,
                'message': ser.errors
            },
            status=400
        )
    

class CashTransactionDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    
    def delete(self, request, id):
        obj = get_object_or_404(CashTransaction, id=id)
        obj.delete()
        return Response(
            {
                'success': True,
                'message': 'Cash Transaction deleted'
            },
            status=204
        )