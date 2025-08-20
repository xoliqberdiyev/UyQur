from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Offer, Order
from core.apps.counterparty.models import Counterparty


class OfferCreateSerializer(serializers.Serializer):
    counterparty_id = serializers.UUIDField()
    price = serializers.IntegerField()
    phone = serializers.CharField(required=False)
    comment = serializers.CharField(required=False)
    qqs = serializers.CharField(required=False)
    price_type = serializers.ChoiceField(Offer.PRICE_TYPE)

    def validate(self, data):
        counterparty = Counterparty.objects.filter(id=data['counterparty_id']).first()
        if not counterparty:
            raise serializers.ValidationError("Counterparty not found")
        data['counterparty']
        return data


class MultipleOfferCreateSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    offers = serializers.ListSerializer(child=OfferCreateSerializer())

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
                offer.append(
                    Offer(
                        counterparty=offer['counterparty'],
                        price=offer['price'],
                        phone=offer.get('phone'),
                        comment=offer.get('comment'),
                        qqs=offer.get('qqs'),
                        price_type=offer.get('price_type')
                    )
                )
            
            return Offer.objects.bulk_update(offers)


class OfferListSerializer(serializers.ModelSerializer):
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')

    class Meta:
        model = Offer
        fields = [
            'id', 'counterparty', 'price', 'number', 'phone', 'comment', 'qqs', 'price_type'
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