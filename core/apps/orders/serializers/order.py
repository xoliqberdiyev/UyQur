from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Order, OrderApplication
from core.apps.products.models import Product, Unity
from core.apps.wherehouse.models import WhereHouse
from core.apps.projects.models import Project, ProjectDepartment


class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    unity_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    wherehouse_id = serializers.UUIDField()
    project_id = serializers.UUIDField()
    project_department_id = serializers.UUIDField(required=False)
    date = serializers.DateField()

    def validate(self, data):
        try:
            product = Product.objects.get(id=data['product_id'])
            unity = Unity.objects.get(id=data['unity_id'])
            wherehouse = WhereHouse.objects.get(id=data['wherehouse_id'])
            project = Project.objects.get(id=data['project_id'])
            if data.get('project_department_id'):
                project_department = ProjectDepartment.objects.get(
                    id=data['project_department_id']
                )
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        except Unity.DoesNotExist:
            raise serializers.ValidationError("Unity not found")
        except WhereHouse.DoesNotExist:
            raise serializers.ValidationError("Where House not found")
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project not found")
        try:
            if data.get('project_department_id'):
                data['project_department'] = ProjectDepartment.objects.get(id=data['project_department_id'])
        except ProjectDepartment.DoesNotExist:
            raise serializers.ValidationError("Project Department not found")
        
        data['product'] = product
        data['unity'] = unity
        data['wherehouse'] = wherehouse
        data['project'] = project
        return data
    

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