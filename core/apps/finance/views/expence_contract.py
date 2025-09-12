from rest_framework import generics, views 
from rest_framework.response import Response

from core.apps.finance.models import ExpenceContract
from core.apps.finance.serializers.expence_contract import ExpenceContractSerializer
from core.apps.accounts.permissions.permissions import HasRolePermission


class ExpenceContractCreateApiView(generics.GenericAPIView):
    serializer_class = ExpenceContractSerializer
    queryset = ExpenceContract.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    'success': True, 
                    'message': 'Expence Contract created successfully'
                },
                status=201
            )
        return Response(
            {
                'success': False,
                'message': 'Expence Contract create failed',
                'error': serializer.errors,
            },
            status=400
        )


class ExpenceContractListApiView(generics.GenericAPIView):
    serializer_class = ExpenceContractSerializer
    queryset = ExpenceContract.objects.select_related(
        'project_folder', 'project', 'user', 'expence_type', 'counterparty'
    )
    permission_classes = [HasRolePermission]

    def get(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)