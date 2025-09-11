from django.db.models import Sum 
from django.shortcuts import get_object_or_404

from rest_framework import generics, views, filters
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination
from core.apps.counterparty.models import Counterparty, CounterpartyFolder
from core.apps.counterparty.serializers import counterparty as serializers
from core.apps.counterparty.filters.counterparty import CounterpartyFilter


class CounterpartyListApiView(generics.ListAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.exclude(is_archived=True).exclude(folder__isnull=False)
    pagination_class = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CounterpartyFilter
    search_fields = [
        'name', 'inn'
    ]


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


class FolderCounterpartyListApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.exclude(is_archived=True)
    permission_classes = [HasRolePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', 'inn'
    ]

    def get(self, reuqest, folder_id):
        folder = get_object_or_404(CounterpartyFolder, id=folder_id)
        queryset = self.queryset.filter(folder=folder).exclude(folder__isnull=True)
        page = self.paginate_queryset(self.filter_queryset(queryset))
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
    

class CounterpartyStatisticsApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def get(self, request):
        counterparty_ids = request.query_params.getlist('counterparty')
        if counterparty_ids:
            queryset = Counterparty.objects.filter(id__in=counterparty_ids)
        else:
            queryset = Counterparty.objects.all()
        
        res = queryset.aggregate(
            kredit_usd=Sum('kredit_usd'),
            kredit_uzs=Sum('kredit_uzs'),
            total_kredit=Sum('total_kredit'),
            debit_usd=Sum('debit_usd'),
            debit_uzs=Sum('debit_uzs'),
            total_debut=Sum('total_debit'),
        )
        return Response(res)


class CounterpartiesApiView(generics.GenericAPIView):
    serializer_class = serializers.CounterpartyListSerializer
    queryset = Counterparty.objects.all()
    permission_classes = [HasRolePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', 'inn'
    ]

    def get(self, request):
        page = self.paginate_queryset(self.filter_queryset(self.queryset))
        if page is not None:
            ser = self.serializer_class(page, many=True)
            return self.get_paginated_response(ser.data)
        