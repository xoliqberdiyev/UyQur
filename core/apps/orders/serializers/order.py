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
from core.apps.projects.models import Project, ProjectFolder
from core.apps.projects.serializers.project import ProjectListSerializer



class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    unity_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    wherehouse_id = serializers.UUIDField()
    project_id = serializers.UUIDField(required=False)
    project_folder_id = serializers.UUIDField()
    date = serializers.DateField()

    def validate(self, data):
        try:
            product = Product.objects.get(id=data['product_id'])
            unity = Unity.objects.get(id=data['unity_id'])
            wherehouse = WhereHouse.objects.get(id=data['wherehouse_id'])
            project_folder = ProjectFolder.objects.get(id=data['project_folder_id'])
            if data.get('project_id'):
                Project.objects.get(
                    id=data['project_id']
                )
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        except Unity.DoesNotExist:
            raise serializers.ValidationError("Unity not found")
        except WhereHouse.DoesNotExist:
            raise serializers.ValidationError("Where House not found")
        except ProjectFolder.DoesNotExist:
            raise serializers.ValidationError("Project Folder not found")
        try:
            if data.get('project_id'):
                data['project'] = Project.objects.get(id=data['project_id'])
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project not found")
        
        data['product'] = product
        data['unity'] = unity
        data['wherehouse'] = wherehouse
        data['project_folder'] = project_folder
        return data

    def create(self, validated_data):
        with transaction.atomic():
            order = Order.objects.create(
                product=validated_data.get('product'),
                unity=validated_data.get('unity'),
                wherehouse=validated_data.get('wherehouse'),
                project_folder=validated_data.get('project_folder'),
                project=validated_data.get('project'),
                quantity=validated_data.get('quantity'),
                date=validated_data.get('date'),
                employee=self.context.get('user'),
            )
            return order


class MultipleOrderCreateSerializer(serializers.Serializer):
    resources = serializers.ListSerializer(child=OrderCreateSerializer())


class OrderListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    unity = UnityListSerializer()
    project = ProjectListSerializer()
    wherehouse = WhereHouseListSerializer()
    project_folder = ProjectFolder()

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'unity', 'quantity', 'project', 'project_folder',
            'wherehouse', 'date', 'status', 'employee'
        ]


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product', 'unity', 'quantity', 'project', 'project_folder', 'wherehouse', 'date',
        ]