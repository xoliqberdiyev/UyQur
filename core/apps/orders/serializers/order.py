from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Order
# products
from core.apps.products.models import Product, Unity
from core.apps.products.serializers.product import ProductListSerializer
from core.apps.products.serializers.unity import UnityListSerializer
# wherehouse
from core.apps.wherehouse.models import WhereHouse
from core.apps.wherehouse.serializers.wherehouse import WhereHouseListSerializer
# projects
from core.apps.projects.models import Project, ProjectDepartment
from core.apps.projects.serializers.project import (
    ProjectListSerializer, 
    ProjectDepartmentListSerializer
)



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
                ProjectDepartment.objects.get(
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

    def create(self, validated_data):
        with transaction.atomic():
            order = Order.objects.create(
                product=validated_data.get('product'),
                unity=validated_data.get('unity'),
                wherehouse=validated_data.get('wherehouse'),
                project=validated_data.get('project'),
                project_department=validated_data.get('project_department'),
                quantity=validated_data.get('quantity'),
                date=validated_data.get('date')
            )
            return order


class OrderListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    unity = UnityListSerializer()
    project = ProjectListSerializer()
    project_department = ProjectDepartmentListSerializer()
    wherehouse = WhereHouseListSerializer()

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'unity', 'quantity', 'project', 'project_department',
            'wherehouse', 'date', 'status', 'employee'
        ]