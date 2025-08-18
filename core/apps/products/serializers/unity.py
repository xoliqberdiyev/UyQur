from rest_framework import serializers

from core.apps.products.models import Unity


class UnityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unity
        fields = ['id', 'value']
    
    def create(self, validated_data):
        return Unity.objects.create(**validated_data)