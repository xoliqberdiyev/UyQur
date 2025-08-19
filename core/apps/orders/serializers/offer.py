from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Offer, Order


class OfferCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    phone = serializers.CharField(required=False)
    comment = serializers.CharField(required=False)
    qqs = serializers.CharField(required=False)
    price_type = serializers.ChoiceField(Offer.PRICE_TYPE)


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
                        name=offer['name'],
                        price=offer['price'],
                        phone=offer.get('phone'),
                        comment=offer.get('comment'),
                        qqs=offer.get('qqs'),
                        price_type=offer.get('price_type')
                    )
                )
            
            return Offer.objects.bulk_update(offers)


class OfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'id', 'name', 'price', 'number', 'phone', 'comment', 'qqs', 'price_type'
        ]


class OfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'name', 'price', 'number', 'phone', 'comment', 'qqs', 'price_type'
        ]
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.number = validated_data.get('number', instance.number)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.qqs = validated_data.get('qqs', instance.qqs)
        instance.price_type = validated_data.get('price_type', instance.price_type)
        instance.save()
        return instance