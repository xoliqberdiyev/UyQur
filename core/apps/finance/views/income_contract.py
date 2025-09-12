from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.finance.models import IncomeContract
from core.apps.finance.serializers.income_contract import IncomeContractSerializer, IncomeContractCreateSerializer


class IncomeContractCreateApiView(generics.GenericAPIView):
    serializer_class = IncomeContractCreateSerializer
    queryset = IncomeContract.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Income Contract created successfully',
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'Income Contract create failed',
                'error': serializer.errors,
            },
            status=400
        )


class IncomeContractListApiView(generics.GenericAPIView):
    serializer_class = IncomeContractSerializer
    queryset = IncomeContract.objects.select_related(
        'project_folder', 'project', 'income_type', 'counterparty',
    )
    permission_classes = [HasRolePermission]

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
