from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination
from core.apps.counterparty.models import Counterparty
from core.apps.counterparty.serializers import counterparty as serializers


class CounterpartyListApiView(generics.ListAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.exclude(is_archived=True)
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
    

class ArchiveCounterpartyApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = []

    def get(self, request, id):
        counterparty = get_object_or_404(Counterparty, id=id)
        counterparty.is_archived = True
        counterparty.save()
        return Response(
            {'success': True, 'message': 'counterparty archived'},
            status=200
        )
    

class ArchivedCounterpartyListApiView(generics.ListAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.exclude(is_archived=False)
    pagination_class = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination