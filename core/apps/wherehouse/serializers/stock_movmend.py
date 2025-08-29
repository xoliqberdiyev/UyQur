from django.db import transaction

from rest_framework import serializers

from core.apps.wherehouse.models import StockMovemend, StockMovmendProduct, Inventory, WhereHouse
from core.apps.products.models import Unity, Product
from core.apps.projects.models import ProjectFolder, Project


class StockMovmendProductSerializer(serializers.Serializer):
    inventory_id = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        inventory = Inventory.objects.filter(id=data['inventory_id']).first()
        if not inventory:
            raise serializers.ValidationError("Inventory not found")
        data['inventory'] = inventory
        return data


class StockMovmendCreateSerializer(serializers.Serializer):
    products = StockMovmendProductSerializer(many=True)
    project_folder_id = serializers.UUIDField(required=False)
    project_id = serializers.UUIDField(required=False)
    wherehouse_to_id = serializers.UUIDField()
    wherehouse_from_id = serializers.UUIDField()
    date = serializers.DateField(required=False)
    comment = serializers.CharField(required=False)

    def validate(self, data):
        if data.get('project_folder_id'):
            project_folder = ProjectFolder.objects.filter(id=data['project_folder_id']).first()
            if not project_folder:
                raise serializers.ValidationError("Project Folder not found")
            data['project_folder'] = project_folder
        if data.get('project_id'):
            project = Project.objects.filter(id=data['project_id']).first()
            if not project:
                raise serializers.ValidationError("Project not found")
            data['project'] = project
        wherehouse_to = WhereHouse.objects.filter(id=data['wherehouse_to_id']).first()
        if not wherehouse_to:
            raise serializers.ValidationError("WhereHouse to not found")
        wherehouse_from = WhereHouse.objects.filter(id=data['wherehouse_from_id']).first()
        if not wherehouse_from:
            raise serializers.ValidationError("WhereHouse from not found")
        data['wherehouse_to'] = wherehouse_to
        data['wherehouse_from'] = wherehouse_from
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            products = validated_data.pop('products')
            stock_movemend = StockMovemend.objects.create(
                project_folder=validated_data.get('project_folder'),
                project=validated_data.get('project'),
                date=validated_data.get('date'),
                comment=validated_data.get('comment'),
                wherehouse_to=validated_data.get('wherehouse_to'),
                wherehouse_from=validated_data.get('wherehouse_from'),
            )
            movmend_products = []
            for product in products:
                    movmend_products.append(StockMovmendProduct(
                    inventory=product.get('inventory'),
                    quantity=product.get('quantity'),
                    stock_movemend=stock_movemend,
                ))
            StockMovmendProduct.objects.bulk_create(movmend_products)
            return stock_movemend   
            

class StockMovemendProductListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='get_product')
    unity = serializers.SerializerMethodField(method_name='get_unity')

    class Meta:
        model = StockMovmendProduct
        fields = [
            'id', 'product', 'unity', 'quantity'
        ]

    def get_product(self, obj):
        return {
            'id': obj.inventory.product.id,
            'name': obj.inventory.product.name,
            'type': obj.inventory.product.type,
        }

    def get_unity(self, obj):
        return {
            'id': obj.inventory.unity.id,
            'value': obj.inventory.unity.value,
        }


class StockMovemendListSerializer(serializers.ModelSerializer):
    movmend_products = StockMovemendProductListSerializer(many=True)
    wherehouse_to = serializers.SerializerMethodField(method_name='get_wherehouse_to')
    wherehouse_from = serializers.SerializerMethodField(method_name='get_wherehouse_from')
    recipient = serializers.SerializerMethodField(method_name='get_recipient')
    project_folder = serializers.SerializerMethodField(method_name='get_project_folder')
    project = serializers.SerializerMethodField(method_name='get_project')
    
    class Meta:
        model = StockMovemend
        fields = [
            'id', 'number', 'wherehouse_to', 'wherehouse_from', 'recipient', 'project_folder',
            'project', 'movemend_type', 'date', 'comment', 'movmend_products'
        ]
    
    def get_wherehouse_to(self, obj):
        return {
            'id': obj.wherehouse_to.id,
            'name': obj.wherehouse_to.name,
        }

    def get_wherehouse_from(self, obj):
        return {
            'id': obj.wherehouse_from.id,
            'name': obj.wherehouse_from.name,
        }
    
    def get_recipient(self, obj):
        return {
            'id': obj.recipient.id,
            'full_name': obj.recipient.full_name,
        } if obj.recipient else None
    
    def get_project_folder(self, obj):
        return {
            'id': obj.project_folder.id,
            'name': obj.project_folder.name
        }

    def get_project(self, obj):
        return {
            'id': obj.project.id,
            'name': obj.project.name
        } if obj.project else None