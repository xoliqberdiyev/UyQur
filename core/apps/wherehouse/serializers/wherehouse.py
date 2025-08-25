from django.db import transaction

from rest_framework import serializers

from core.apps.wherehouse.models.wherehouse import WhereHouse
from core.apps.wherehouse.serializers.inventory import InventoryListSerializer
from core.apps.company.serializers.branch import BranchListSerializer
from core.apps.company.models import Branch


class WhereHouseListSerializer(serializers.ModelSerializer):
    branch = BranchListSerializer()

    class Meta:
        model = WhereHouse
        fields = [
            'id', 'name', 'address', 'branch'
        ]


class WhereHouseDetailSerializer(serializers.ModelSerializer):
    branch = BranchListSerializer()

    class Meta:
        model = WhereHouse
        fields = [
            'id', 'name', 'address', 'branch',
        ]


class WhereHouseCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    branch_id = serializers.UUIDField()

    def validate(self, data):
        branch = Branch.objects.filter(id=data.get('branch_id')).first()
        if not branch:
            raise serializers.ValidationError("Branch not found")
        data['branch'] = branch
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return WhereHouse.objects.create(
                name=validated_data.get('name'),
                address=validated_data.get('address'),
                branch=validated_data.get('branch'),
            )


class WhereHouseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhereHouse
        fields = [
            'name', 'address', 'branch'
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.branch = validated_data.get('branch', instance.branch)
        instance.save()
        return instance
