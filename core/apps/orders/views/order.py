from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views, filters
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from core.apps.orders.serializers import order as serializers
from core.apps.orders.models import Order
from core.apps.orders.filters.order import OrderFilter
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class OrderListApiView(generics.ListAPIView):
    serializer_class = serializers.OrderListSerializer
    queryset = Order.objects.select_related(
        'product', 'unity', 'project', 'project_folder', 'wherehouse'
    )
    permission_classes = [HasRolePermission]
    required_permissions = ['order']
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        'product__name', 'unity__value', 'project_folder__name', 'project__name',
        'wherehouse__name', 'date', 'quantity', 'employee__full_name', 'employee__phone_number'
    ]
    filterset_class = OrderFilter


class OrderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.MultipleOrderCreateSerializer
    queryset = Order.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['order']

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': 'orders successfully created'}, status=201)
        return Response({'success': False, 'error':serializer.errors}, status=400)
    

class OrderUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.OrderUpdateSerializer
    queryset = Order.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['order']
    lookup_field = 'id'


class OrderDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['order']

    def delete(self, request, id):
        order = get_object_or_404(Order, id=id)
        order.delete()
        return Response({"success": True, "message": "Deleted!"}, status=204)


class OrderChangeStatusCancelledApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['order']

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.status = 'CANCELLED'
        order.save()
        return Response(
            {'success': True, 'message': 'order cancelled'}, 
            status=200
        )


class OrderChangeStatusAcceptedApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['order']

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.status = 'ACCEPTED'
        order.save()
        return Response(
            {'success': True, 'message': 'order accepted'}, 
            status=200
        )
    

class OrderAcceptApiView(generics.ListAPIView):
    serializer_class = serializers.OrderListSerializer
    queryset = Order.objects.filter(status='ACCEPTED')
    permission_classes = [HasRolePermission]
    required_permissions = ['order']
    pagination_class = CustomPageNumberPagination