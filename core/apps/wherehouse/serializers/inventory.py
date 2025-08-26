from rest_framework import serializers

from core.apps.wherehouse.models.inventory import Inventory


class InventoryListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='get_product')
    unity = serializers.SerializerMethodField(method_name='get_unity')

    class Meta:
        model = Inventory
        fields = [
            'id', 'quantity', 'product', 'price', 'unity'
        ]

    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'type': obj.product.type
        }
    
    def get_unity(self, obj):
        return {
            'id': obj.unity.id,
            'value': obj.unity.value,
        }