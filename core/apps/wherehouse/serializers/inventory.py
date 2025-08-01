from rest_framework import serializers

from core.apps.wherehouse.models.inventory import Inventory


class WhereHouseInventoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'id', 'quantity', 'product'
        ]