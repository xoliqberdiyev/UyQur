from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Party, PartyAmount, Order, DeletedParty
from core.apps.orders.serializers.order import MultipleOrderAddSerializer, OrderListSerializer
from core.apps.accounts.models import User


class PartyCreateSerializer(serializers.Serializer):
    resources = MultipleOrderAddSerializer(many=True)
    mediator_id = serializers.UUIDField()
    delivery_date = serializers.DateField()
    payment_date = serializers.DateField()
    comment = serializers.CharField(required=False)
    discount = serializers.IntegerField(required=False)
    discount_currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')], required=False)
    audit = serializers.ChoiceField(
        choices=[('CHECKED', 'tekshirildi'),('PROCESS', 'jarayonda')], required=False
    )
    audit_comment = serializers.CharField(required=False)

    def validate(self, data):
        user = User.objects.filter(id=data['mediator_id']).first()
        if not user:
            raise serializers.ValidationError("User not found")
        data['user'] = user
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            resources = validated_data.pop('resources')
            orders = []
            total_price = 0
            for resource in resources:
                orders.append(Order(
                    product=resource['product'],
                    unity=resource['unity'],
                    project_folder=resource.get('project_folder'),
                    project=resource.get('project'),
                    counterparty=resource.get('counterparty'),
                    wherehouse=resource.get('wherehouse'),
                    quantity=resource.get('quantity'),
                    unit_amount=resource.get('unit_amount'),
                    currency=resource.get('currency'),
                    amount=resource.get('amount'), 
                    employee=self.context.get('user'),
                    qqs_price=resource.get('qqs_price'),
                    total_price=resource.get('total_price'),
                    qqs=resource.get('qqs'),
                ))
                total_price += resource.get('amount')
            created_orders = Order.objects.bulk_create(orders)
            party = Party.objects.create(
                mediator=validated_data.get('user'),
                delivery_date=validated_data.get('delivery_date'),
                payment_date=validated_data.get('payment_date'),
                comment=validated_data.get('comment'),
                audit=validated_data.get('audit'),
                audit_comment=validated_data.get('audit_comment'),
                discount=validated_data.get('discount'),
                discount_currency=validated_data.get('discount_currency'),
            )
            party.orders.add(*created_orders)
            party.save()
            PartyAmount.objects.create(
                total_price=total_price,
                party=party,
            )
            return party


class PartyAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartyAmount
        fields = [
            'id', 'total_price', 'cost_amount', 'calculated_amount', 'paid_amount', 'payment_amount'
        ]


class PartyDetailSerializer(serializers.ModelSerializer):
    orders = OrderListSerializer(many=True)
    party_amount = PartyAmountSerializer()

    class Meta:
        model = Party
        fields = [
            'id', 'number', 'delivery_date', 'closed_date', 'order_date', 'payment_date', 'status',
            'payment_status', 'process', 'confirmation', 'comment', 'audit', 'audit_comment',
            'orders', 'party_amount'
        ]


class PartyListSerializer(serializers.ModelSerializer):
    party_amount = PartyAmountSerializer()

    class Meta:
        model = Party
        fields = [
            'id','number', 'delivery_date', 'closed_date', 'order_date', 'payment_date', 'status',
            'payment_status', 'process', 'confirmation', 'comment', 'audit', 'audit_comment',
            'party_amount'
        ]


class DeletedPartyCreateSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False)

    def validate(self, data):
        party = Party.objects.filter(id=self.context.get('party_id')).first()
        if not party:
            raise serializers.ValidationError("Party not found")
        data['party'] = party
        return data

    def create(self, validated_data):
        with transaction.atomic():
            return DeletedParty.objects.create(
                comment=validated_data.get('comment'),
                party=validated_data.get('party')
            )
    

class DeletedPartyListSerializer(serializers.ModelSerializer):
    party_number = serializers.IntegerField(source='party.number')
    party_total_price = serializers.IntegerField(source='party.party_amount.total_price')
    mediator = serializers.SerializerMethodField(method_name='get_mediator')

    class Meta:
        model = DeletedParty
        fields = [
            'id', 'deleted_date', 'party_number', 'party_total_price', 'mediator'
        ]
    
    def get_mediator(self, obj):
        return {
            'id': obj.party.mediator.id,
            'name': obj.party.mediator.full_name
        }
    

class PartyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = [
            'mediator', 'delivery_date', 'payment_date',
        ]
        extra_kwargs = {
            'mediator': {'required': False}, 
            'delivery_date': {'required': False}, 
            'payment_date': {'required':False}
        }

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.mediator = validated_data.get('mediator', instance.mediator)
            instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
            instance.payment_date = validated_data.get('payment_date', instance.payment_date)
            instance.save()
            return instance