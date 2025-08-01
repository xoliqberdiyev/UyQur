from rest_framework import serializers

from core.apps.wherehouse.models.wherehouse import WhereHouse
from core.apps.wherehouse.serializers.inventory import WhereHouseInventoryListSerializer
from core.apps.company.serializers.branch import BranchListSerializer


class WhereHouseListSerializer(serializers.ModelSerializer):
    branch = BranchListSerializer()

    class Meta:
        model = WhereHouse
        fields = [
            'id', 'name', 'address', 'branch'
        ]


class WhereHouseDetailSerializer(serializers.ModelSerializer):
    branch = BranchListSerializer()
    inventories = WhereHouseInventoryListSerializer(many=True)

    class Meta:
        model = WhereHouse
        fields = [
            'id', 'name', 'address', 'branch', 'inventories'
        ]

