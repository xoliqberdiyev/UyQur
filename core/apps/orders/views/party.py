from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from django_filters.rest_framework.backends import DjangoFilterBackend

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.orders.serializers import party as serializers
from core.apps.orders.models import Party, PartyAmount, DeletedParty, Order
from core.apps.orders.filters.party import PartyFilter
from core.apps.orders.tasks.order import create_inventory
from core.apps.finance.models import Expence


class PartyCreateApiView(generics.GenericAPIView):
    serializer_class = serializers.PartyCreateSerializer
    queryset = Party.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['party']

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
    queryset = Party.objects.select_related('party_amount').exclude(is_deleted=True)
    permission_classes = [HasRolePermission]
    required_permissions = ['party']
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
    required_permissions = ['party']
    serializer_class = serializers.PartyDetailSerializer
    queryset = Party.objects.select_related('party_amount').prefetch_related('orders')

    def get(self, request, id):
        party = Party.objects.select_related('party_amount').prefetch_related('orders').filter(id=id).first()
        if not party:
            return Response({'success': False, 'message': 'party not found'}, status=404)
        serializer = self.serializer_class(party)
        return Response(serializer.data, status=200)
    

class PartyDeleteApiView(generics.GenericAPIView):
    serializer_class = serializers.DeletedPartyCreateSerializer
    queryset = Party.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['party']

    def post(self, request, party_id):
        serializer = self.serializer_class(data=request.data, context={'party_id': party_id})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {'success': True, 'message': 'Party deleted'},
                status=200
            )
        return Response(
            {'success': False, 'message': 'error while deletign party', 'error': serializer.errors},
            status=400
        )


class DeletedPartyListApiView(generics.GenericAPIView):
    serializer_class = serializers.DeletedPartyListSerializer
    queryset = DeletedParty.objects.select_related('party')
    permission_classes = [HasRolePermission]
    required_permissions = ['party']

    def get(self, request):
        deleted_parties = DeletedParty.objects.select_related('party')
        page = self.paginate_queryset(deleted_parties)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data, status=200)
    

class PartyUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.PartyUpdateSerializer
    queryset = Party.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['party']
    pagination_class = None

    def patch(self, request, id):
        party = get_object_or_404(Party, id=id)
        serializer = self.serializer_class(data=request.data, instance=party, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'success': True, 'message': 'update',
            }, status=200)
        return Response({'success': False, 'error': serializer.errors}, status=400)
    

class OrderDeleteToPartyApiView(generics.GenericAPIView):
    serializer_class = None
    permission_classes = [HasRolePermission]
    required_permissions = ['party']
    queryset = None
    

    def delete(self, request, party_id, order_id):
        party = get_object_or_404(Party, id=party_id)

        order = party.orders.filter(id=order_id).first()
        if not order:
            return Response(
                {'success': False, 'error_message': 'Order does not belong to the party'},
                status=400
            )

        party.orders.remove(order)
        return Response({'success': True, 'message': 'Order removed from party'}, status=200)
    

class PartyChangeStatusToIsMadeApiView(generics.GenericAPIView):
    serializer_class = None
    queryset = Party.objects.all()
    permission_classes = [HasRolePermission]
    required_permission = ['party']
    pagination_class = None

    def get(self, request, party_id):
        party = get_object_or_404(Party, id=party_id)
        party.status = 'PARTY_IS_MADE'
        party.save()
        for order in party.orders.all():
            create_inventory.delay(
                order.wherehouse.id,
                order.quantity, 
                order.product.id, 
                order.unity.id, 
                order.unit_amount * order.quantity,
                order.project_folder.id if order.project_folder else None,
                order.project.id if order.project else None,
                order.unit_amount,
            )
        return Response(
            {'success': True, 'message': 'party updated'},
            status=200
        )
    

class PartyPaymentApiView(generics.GenericAPIView):
    serializer_class = serializers.PartyExpenceCreateSerializer
    queryset = Expence.objects.all()
    permission_classes = [HasRolePermission]

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(
                {
                    'success': True,
                    'message': 'partiyage tolov qilindi'
                },
                status=200
            )
        return Response(
            {
                'success': False,
                'message': 'partiyaga tolov qilishda xatolik yuz berdi',
                'error': ser.errors,
            },
            status=400
        )