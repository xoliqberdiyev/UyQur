from django.db import transaction

from rest_framework import serializers

from core.apps.wherehouse.models import InvalidProduct, Inventory
from core.apps.projects.models import ProjectFolder, EstimateWork
from core.apps.wherehouse.serializers.inventory import InventoryListSerializer
from core.apps.accounts.serializers.user import UserListSerializer


class InvalidProductCreateSerializer(serializers.Serializer):
    inventory_id = serializers.UUIDField()
    project_folder_id = serializers.UUIDField()
    witnesses_ids = serializers.ListField(child=serializers.UUIDField())
    work_id = serializers.UUIDField(required=False)
    amount = serializers.IntegerField()
    status = serializers.ChoiceField(choices=InvalidProduct.STATUS)
    created_date = serializers.DateField(required=False)
    expiry_date = serializers.DateField(required=False)
    comment = serializers.CharField(required=False)
    file = serializers.FileField(required=False)

    def validate(self, attrs):
        inventory = Inventory.objects.filter(id=attrs['inventory_id']).first()
        if not inventory:
            raise serializers.ValidationError("Inventory not found")
        project_folder = ProjectFolder.objects.filter(id=attrs['project_folder_id']).first()
        if not project_folder:
            raise serializers.ValidationError("Project Folder not found")
        if attrs.get('work_id'):
            work = EstimateWork.objects.filter(id=attrs['work_id']).first()
            if not work:
                raise serializers.ValidationError("Work not found")
            attrs['work'] = work
        attrs['inventory'] = inventory
        attrs['project_folder'] = project_folder
        return super().validate(attrs)
    
    def create(self, validated_data):
        with transaction.atomic():
            witnesses_ids = validated_data.pop('witnesses_ids')
            invalid_product = InvalidProduct.objects.create(
                inventory=validated_data.get('inventory'),
                project_folder=validated_data.get('project_folder'),
                work=validated_data.get('work'),
                amount=validated_data.get('amount'),
                status=validated_data.get('status'),
                created_date=validated_data.get('created_date'),
                expiry_date=validated_data.get('expiry_date'),
                comment=validated_data.get('comment'),
                file=validated_data.get('file'),
            )
            invalid_product.witnesses.set(witnesses_ids)
            invalid_product.inventory.is_invalid = True
            invalid_product.inventory.quantity -= validated_data.get('amount')
            invalid_product.inventory.save()
            invalid_product.save()
            return invalid_product


class InvliadProductListSerializer(serializers.ModelSerializer):
    inventory = InventoryListSerializer()
    project_folder = serializers.SerializerMethodField(method_name='get_folder')
    witnesses = UserListSerializer(many=True)

    class Meta:
        model = InvalidProduct
        fields = [
            'id', 'status', 'inventory', 'project_folder', 'witnesses', 'work', 'amount', 
            'created_date', 'expiry_date', 'comment', 'file'
        ]
    
    def get_folder(self, obj):
        return {
            'id': obj.project_folder.id,
            'name': obj.project_folder.name,
        }