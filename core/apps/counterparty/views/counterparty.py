from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination
from core.apps.counterparty.models import Counterparty
from core.apps.counterparty.serializers import counterparty as serializers
from core.apps.counterparty.filters.counterparty import CounterpartyFilter

class CounterpartyListApiView(generics.ListAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.exclude(is_archived=True)
    pagination_class = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CounterpartyFilter


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


class CounterpartyDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = []

    def delete(self, request, id):
        counterparty = get_object_or_404(Counterparty, id=id)
        counterparty.delete()
        return Response(
            {'success': True, 'message': 'counterparty deleted'},
            status=204
        )
    

class CounterpartyUpdateApiView(generics.UpdateAPIView):
    permission_classes = [HasRolePermission]
    required_permissions = []
    lookup_field = 'id'
    serializer_class = serializers.CounterpartyUpdateSerializer
    queryset = Counterparty.objects.all()
