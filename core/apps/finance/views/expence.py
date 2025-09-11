from rest_framework import generics, views, parsers
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.finance.models import Expence
from core.apps.finance.serializers import expence as serializers


class ExpenceCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.ExpenceCreateSerializer
    queryset = Expence.objects.select_related(
        'cash_transaction', 'payment_type', 'project_folder', 'project',
        'counterparty', 'expence_type', 'user'
    )
    permission_classes = [HasRolePermission]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Expence created'
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'Expence create failed',
                'error': serializer.errors
            },
            status=400
        )


class ExpenceListApiView(generics.GenericAPIView):
    serializer_class = serializers.ExpenceListSerializer
    queryset = Expence.objects.select_related(
        'cash_transaction', 'payment_type', 'project_folder', 'project',
        'counterparty', 'expence_type',
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
        