from rest_framework import generics

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