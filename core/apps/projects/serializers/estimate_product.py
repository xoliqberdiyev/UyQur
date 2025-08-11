from django.db import transaction

from rest_framework import serializers

from core.apps.projects.models.project_estimate import EstimateProduct, EstimateWork
from core.apps.products.models import Product, Unity


class EstimateProductListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='get_product')

    class Meta:
        model = EstimateProduct
        fields = [
            'id', 'product', 'quantity', 'price', 'unity', 'price', 'date'
        ]
    
    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'type': obj.product.type
        }


class EstimateProductCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    unity_id = serializers.UUIDField(required=False)
    date = serializers.DateField()
    estimate_work_id = serializers.UUIDField()

    def validate(self, data):
        product = Product.objects.filter(id=data['product_id']).first()
        if not product:
            raise serializers.ValidationError("Product not found")
        estimate_work = EstimateWork.objects.filter(id=data['estimate_work_id']).first()
        if not estimate_work:
            raise serializers.ValidationError("EstimateWork not found")
        if data.get('unity_id'):
            unity = Unity.objects.filter(id=data['unity_id']).first()
            if not unity:
                raise serializers.ValidationError("Unity not found")
            data['unity'] = unity
        data['product'] = product
        data['estimate_work'] = estimate_work
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return EstimateProduct.objects.create(
                product=validated_data.get('product'),
                quantity=validated_data.get('quantity'),
                price=validated_data.get('price'),
                unity=validated_data.get('unity'),
                date=validated_data.get('date'),
                estimate_work=validated_data.get('estimate_work'),
            )


class EstimateProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstimateProduct
        fields = [
            'product', 'quantity', 'price', 'unity', 'date'
        ]

    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.unity = validated_data.get('unity', instance.unity)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance