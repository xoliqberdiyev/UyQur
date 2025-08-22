from rest_framework import generics, views
from rest_framework.response import Response

from django_filters.rest_framework.backends import DjangoFilterBackend

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.orders.serializers import party as serializers
from core.apps.orders.models import Order, Party, PartyAmount
from core.apps.orders.filters.party import PartyFilter


class PartyCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.PartyCreateSerializer
    queryset = Party.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': "party created"},
                status=200
            )
        return Response(
            {'success': False, 'message': 'error while party created', 'error': serializer.errors},
            status=400
        )
    

class PartyListApiView(generics.GenericAPIView):
    serializer_class = serializers.PartyListSerializer
    queryset = Party.objects.select_related('party_amount')
    permission_classes = [HasRolePermission]
    required_permissions = []
    filter_backends = [DjangoFilterBackend]
    filterset_class = PartyFilter
    
    def get(self, request):
        parties = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(parties)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(parties, many=True)
        return Response(serializer.data, status=200)


class PartyDetailApiView(generics.GenericAPIView):
    permission_classes = [HasRolePermission]
    required_permissions = []
    serializer_class = serializers.PartyDetailSerializer
    queryset = Party.objects.select_related('party_amount').prefetch_related('orders')

    def get(self, request, id):
        party = Party.objects.select_related('party_amount').prefetch_related('orders').filter(id=id).first()
        if not party:
            return Response({'success': False, 'message': 'party not found'}, status=404)
        serializer = self.serializer_class(party)
        return Response(serializer.data, status=200)