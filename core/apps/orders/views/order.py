from rest_framework import generics, response
from rest_framework.response import Response

from core.apps.orders.models import Order, OrderApplication
from core.apps.orders.serializers import order as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class OrderApplicationCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.OrderApplicationCreateSerializer
    queryset = OrderApplication.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context