from django.db import transaction

from rest_framework import serializers
# orders
from core.apps.orders.models import Order
from core.apps.orders.tasks.order import create_inventory
# products
from core.apps.products.models import Product, Unity
from core.apps.products.serializers.product import ProductListSerializer
from core.apps.products.serializers.unity import UnityListSerializer
# wherehouse
from core.apps.wherehouse.models import WhereHouse
from core.apps.wherehouse.serializers.wherehouse import WhereHouseListSerializer
# projects
from core.apps.projects.models import Project, ProjectFolder
from core.apps.projects.serializers.project import ProjectListSerializer, ProjectFolderListSerializer
# counterparty
from core.apps.counterparty.models import Counterparty


class OrderCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    unity_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    wherehouse_id = serializers.UUIDField()
    project_id = serializers.UUIDField(required=False)
    project_folder_id = serializers.UUIDField(required=False)

    def validate(self, data):
        try:
            product = Product.objects.get(id=data['product_id'])
            unity = Unity.objects.get(id=data['unity_id'])
            wherehouse = WhereHouse.objects.get(id=data['wherehouse_id'])
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
        try:
            if data.get('project_id'):
                data['project'] = Project.objects.get(id=data['project_id'])
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project not found")
        if data.get('project_folder_id'):
            try:
                project_folder = ProjectFolder.objects.get(id=data['project_folder_id'])
            
            except ProjectFolder.DoesNotExist:
                raise serializers.ValidationError("Project Folder not found")
            data['project_folder'] = project_folder

        data['product'] = product
        data['unity'] = unity
        data['wherehouse'] = wherehouse
        return data


class MultipleOrderCreateSerializer(serializers.Serializer):
    resources = OrderCreateSerializer(many=True)
    date = serializers.DateField()

    def create(self, validated_data):
        with transaction.atomic():
            resources = validated_data.pop('resources')
            common_date = validated_data.get('date')
            orders = []

            for resource in resources:
                orders.append(Order(
                    product=resource['product'],
                    unity=resource['unity'],
                    wherehouse=resource['wherehouse'],
                    project_folder=resource.get('project_folder'),
                    project=resource.get('project'),
                    quantity=resource['quantity'],
                    date=common_date,
                    employee=self.context.get('user'),
                ))
            created_orders = Order.objects.bulk_create(orders)
            return created_orders
    

class OrderListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()
    unity = UnityListSerializer()
    project = ProjectListSerializer()
    wherehouse = WhereHouseListSerializer()
    project_folder = ProjectFolderListSerializer()
    employee = serializers.SerializerMethodField(method_name='get_employee')
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'unity', 'quantity', 'project', 'project_folder',
            'wherehouse', 'date', 'status', 'employee', 'counterparty', 'unit_amount', 'currency',
            'total_price', 'qqs_price', 'amount', 'qqs'
        ]

    def get_employee(self, obj):
        return {
            "id": obj.employee.id,
            "full_name": obj.employee.full_name,
            "phone_number": obj.employee.phone_number
        } if obj.employee else None

    def get_counterparty(self, obj):
        return {
            'id': obj.counterparty.id,
            'name': obj.counterparty.name,
        } if obj.counterparty else None


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product', 'unity', 'quantity', 'project', 'project_folder', 'wherehouse', 'date',
        ]

    
class MultipleOrderAddSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    unity_id = serializers.UUIDField()
    project_folder_id = serializers.UUIDField(required=False)
    project_id = serializers.UUIDField(required=False)
    counterparty_id = serializers.UUIDField()
    wherehouse_id = serializers.UUIDField()
    
    quantity = serializers.IntegerField()
    unit_amount = serializers.IntegerField()
    currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')])
    amount = serializers.IntegerField()
    total_price = serializers.IntegerField(required=False)
    qqs_price = serializers.IntegerField(required=False)
    qqs = serializers.IntegerField(required=False)

    def validate(self, data):
        product = Product.objects.filter(id=data['product_id']).first()
        if not product:
            raise serializers.ValidationError('product not found')
        unity = Unity.objects.filter(id=data['unity_id']).first()
        if not unity:
            raise serializers.ValidationError("Unity not found")
        wherehouse = WhereHouse.objects.filter(id=data['wherehouse_id']).first()
        if not wherehouse:
            raise serializers.ValidationError("WhereHouse not found")
        counterparty = Counterparty.objects.filter(id=data['counterparty_id']).first()
        if not counterparty:
            raise serializers.ValidationError("Counterparty not found")
        if data.get('project_id'):
            project = Project.objects.filter(id=data.get('project_id')).first()
            if not project:
                raise serializers.ValidationError("Project not found")
            data['project'] = project
        if data.get('project_folder_id'):
            project_folder = ProjectFolder.objects.filter(id=data.get('project_folder_id')).first()
            if not project_folder:
                raise serializers.ValidationError("Project Folder not found")
            data['project_folder'] = project_folder
        data['product'] = product
        data['unity'] = unity
        data['wherehouse'] = wherehouse
        data['counterparty'] = counterparty
        return data