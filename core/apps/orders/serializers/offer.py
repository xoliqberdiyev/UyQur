from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Offer, Order
from core.apps.counterparty.models import Counterparty
from core.apps.orders.serializers.order import OrderListSerializer


class OfferCreateSerializer(serializers.Serializer):
    counterparty_id = serializers.UUIDField()
    price = serializers.IntegerField()
    phone = serializers.CharField(required=False)
    comment = serializers.CharField(required=False)
    qqs = serializers.BooleanField(required=False)
    price_type = serializers.ChoiceField(Offer.PRICE_TYPE)

    def validate(self, data):
        counterparty = Counterparty.objects.filter(id=data['counterparty_id']).first()
        if not counterparty:
            raise serializers.ValidationError("Counterparty not found")
        data['counterparty'] = counterparty
        return data


class MultipleOfferCreateSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    offers = OfferCreateSerializer(many=True)

    def validate(self, data):
        order = Order.objects.filter(id=data['order_id']).first()
        if not order:
            raise serializers.ValidationError("Order not found")
        data['order'] = order
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            offers = []
            for offer in validated_data.pop('offers'):
                offers.append(
                    Offer(
                        order=validated_data.get('order'),
                        counterparty=offer['counterparty'],
                        price=offer['price'],
                        phone=offer.get('phone'),
                        comment=offer.get('comment'),
                        qqs=offer.get('qqs'),
                        price_type=offer.get('price_type')
                    )
                )
            
            created_offers = Offer.objects.bulk_create(offers)
            return created_offers

class OfferListSerializer(serializers.ModelSerializer):
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')
    order = OrderListSerializer()

    class Meta:
        model = Offer
        fields = [
            'id', 'counterparty', 'price', 'number', 'phone', 'comment', 'qqs', 'price_type', 'order'
        ]

    def get_counterparty(self, obj):
        return {
            'id': obj.counterparty.id,
            'name': obj.counterparty.name
        }


class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'counterparty', 'price', 'number', 'phone', 'comment', 'qqs', 'price_type'
        ]
    
    def update(self, instance, validated_data):
        instance.counterparty = validated_data.get('counterparty', instance.counterparty)
        instance.price = validated_data.get('price', instance.price)
        instance.number = validated_data.get('number', instance.number)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.qqs = validated_data.get('qqs', instance.qqs)
        instance.price_type = validated_data.get('price_type', instance.price_type)
        instance.save()
        return instance
    

class OffersSerializer(serializers.ModelSerializer):
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')

    class Meta:
        model = Offer
        fields = [
            'id', 'number', 'price', 'price_type', 'phone', 'comment', 'qqs', 'counterparty'
        ]

    def get_counterparty(self, obj):
        return {
            'id': obj.counterparty.id,
            'name': obj.counterparty.name
        }


class OrderListForOfferSerializer(serializers.ModelSerializer):
    offers = OffersSerializer(many=True)
    product = serializers.SerializerMethodField(method_name='get_product')
    unity = serializers.SerializerMethodField(method_name='get_unity')

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'unity', 'quantity', 'date', 'offers'
        ]
    
    def get_product(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'type': obj.product.type,
        }

    def get_unity(self, obj):
        return {
            'id': obj.unity.id,
            'value': obj.unity.value
        }