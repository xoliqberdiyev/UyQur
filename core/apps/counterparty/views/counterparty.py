from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination
from core.apps.counterparty.models import Counterparty
from core.apps.counterparty.serializers import counterparty as serializers


class CounterpartyListApiView(generics.ListAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.all()
    pagination_class = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination


class CounterpartyCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyCreateSerializer
    queryset = Counterparty.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'Conterparty Created'},
                status=201
            )
        return Response(
            {'success': False, 'message': serializer.errors},
            status=400
        )