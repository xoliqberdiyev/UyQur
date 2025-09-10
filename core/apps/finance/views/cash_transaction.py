from django.shortcuts import get_object_or_404
from django.db.models import Sum

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
    queryset = CashTransaction.objects.prefetch_related('employees', 'payment_type')
    pagination_class = CustomPageNumberPagination


class CashTransactionCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.CashTransactionCreateSerializer
    queryset = CashTransaction.objects.prefetch_related('employees', 'payment_type')
    permission_classes = [HasRolePermission]
    required_permissions = ['project', 'project_folder']


class CashTransactionUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.CashTransactionUpdateSerializer
    queryset = CashTransaction.objects.prefetch_related('employees', 'payment_type')
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
    

class CashTransactionStatisticsApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def get(self, request):
        cash_transaction_ids = request.query_params.getlist('cash_transaction')
        if cash_transaction_ids:
            queryset = CashTransaction.objects.filter(id__in=cash_transaction_ids)
        queryset = CashTransaction.objects.all()
        res = queryset.aggregate(
            total_balance_usd=Sum('total_balance_usd'),
            income_balance_usd=Sum('income_balance_usd'),
            expence_balance_usd=Sum('expence_balance_usd'),
            total_balance_uzs=Sum('total_balance_uzs'),
            income_balance_uzs=Sum('income_balance_uzs'),
            expence_balance_uzs=Sum('expence_balance_uzs')
        )

        return Response(res)
    