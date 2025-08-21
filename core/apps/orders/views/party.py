from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.orders.serializers import party as serializers
from core.apps.orders.models import Order, Party, PartyAmount


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
    queryset = Party.objects.select_related('party_amount').prefetch_related('orders')
    permission_classes = [HasRolePermission]
    required_permissions = []
    
    def get(self, request):
        parties = self.get_queryset()
        serializer = self.serializer_class(parties, many=True)
        return Response(serializer.data, status=200)