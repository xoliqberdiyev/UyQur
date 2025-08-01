from rest_framework import serializers

from core.apps.orders.models import OrderApplication, Order
from core.apps.orders.serializers.order import OrderCreateSerializer, OrderListSerializer


class OrderApplicationCreateSerializer(serializers.Serializer):
    orders = serializers.ListSerializer(child=OrderCreateSerializer())

    def create(self, validated_data):
        employee = self.context.get('user')
        orders_data = validated_data.pop('orders')
        application = OrderApplication.objects.create(
            employee=employee, status="NEW"
        )

        order_objs = []
        for order_data in orders_data:
            order_objs.append(Order(
                product=order_data['product'],
                unity=order_data['unity'],
                quantity=order_data['quantity'],
                wherehouse=order_data['wherehouse'],
                project=order_data['project'],
                project_department=order_data.get('project_department'),
                date=order_data['date']
            ))

        created_orders = Order.objects.bulk_create(order_objs)
        application.orders.add(*created_orders)
        return application
    

class OrderApplicationListSerializer(serializers.ModelSerializer):
    orders = OrderListSerializer(many=True)
    
    class Meta:
        model = OrderApplication
        fields = [
            'id', 'employee', 'status', 'orders'
        ]