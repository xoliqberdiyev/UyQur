from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination
from core.apps.counterparty.models import Counterparty
from core.apps.counterparty.serializers import counterparty as serializers


class CounterpartyListApiView(generics.ListAPIView):
    serializer_class = serializers.CounterpartySerializer
    queryset = Counterparty.objects.select_related('person')
    pagination_class = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination


