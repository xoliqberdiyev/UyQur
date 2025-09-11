from django.shortcuts import get_object_or_404

from rest_framework import generics, views, parsers
from rest_framework.response import Response

from core.apps.finance.models import Income
from core.apps.finance.serializers import income as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class IncomeListApiView(generics.GenericAPIView):
    serializer_class = serializers.IncomeListSerializer
    queryset = Income.objects.select_related(
        'cash_transaction', 'payment_type', 'project_folder', 'project', 'counterparty', 'type_income'
    )
    permission_classes = [HasRolePermission]

    def get(self, request):
        cash_transaction_ids = request.query_params.getlist('cash_transaction')
        if cash_transaction_ids:
            self.queryset = self.queryset.filter(cash_transaction__in=cash_transaction_ids)
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)


class IncomeCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.IncomeCreateSerializer
    queryset = Income.objects.all()
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        ser = self.serializer_class(data=request.data, context={'user': request.user})
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response(
                {
                    'success': True,
                    'message': 'income created'
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'income create failed',
                'error': ser.errors,
            },
            status=400
        )

