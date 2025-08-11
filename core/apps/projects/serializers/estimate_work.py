from django.db import transaction

from rest_framework import serializers

from core.apps.projects.models.project_estimate import EstimateWork, ProjectEstimate
from core.apps.products.models.unity import Unity
from core.apps.projects.serializers.estimate_product import EstimateProductListSerializer


class EstimateWorkListSerializer(serializers.ModelSerializer):
    unity = serializers.SerializerMethodField(method_name='get_unity')
    estimate_products = EstimateProductListSerializer(many=True)

    class Meta:
        model = EstimateWork
        fields = [
            'id', 'number', 'name', 'quantity', 'unity', 'price', 'date', 'total_price', 'estimate_products'
        ]

    def get_unity(self, obj):
        return {
            "id": obj.unity.id,
            'value': obj.unity.value
        } if obj.unity else None


class EstimateWorkCreateSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    unity_id = serializers.UUIDField(required=False)
    price = serializers.IntegerField(required=False)
    date = serializers.DateField(required=False)
    total_price = serializers.IntegerField(required=False)
    estimate_id = serializers.UUIDField()

    def validate(self, data):
        unity_id = data.get('unity_id')
        if unity_id:
            unity = Unity.objects.filter(id=unity_id).first()
            if not unity:
                raise serializers.ValidationError("Unity not found")
            data['unity'] = unity
        estimate = ProjectEstimate.objects.filter(id=data['estimate_id']).first()
        if not estimate:
            raise serializers.ValidationError("estimate not found")
        data['estimate'] = estimate
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            estimate_work = EstimateWork.objects.create(
                number=validated_data.get('number'),
                name=validated_data.get('name'),
                quantity=validated_data.get('quantity'),
                unity=validated_data.get('unity'),
                price=validated_data.get('price'),
                date=validated_data.get('date'),
                total_price=validated_data.get('total_price'),
                estimate=validated_data.get('estimate')
            )
            return estimate_work
    

class EstimateWorkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimateWork
        fields = [
            'name', 'quantity', 'price', 'unity', 'date', 'total_price',
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.unity = validated_data.get('unity', instance.unity)
        instance.date = validated_data.get('date', instance.date)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()
        return instance
    
