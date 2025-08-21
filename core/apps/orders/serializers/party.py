from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Party, PartyAmount, Order
from core.apps.orders.serializers.order import MultipleOrderAddSerializer
from core.apps.accounts.models import User


class PartyCreateSerializer(serializers.Serializer):
    resources = MultipleOrderAddSerializer(many=True)
    mediator_id = serializers.UUIDField()
    delivery_date = serializers.DateField()
    payment_date = serializers.DateField()
    comment = serializers.CharField(required=False)

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
                    total_price=resource.get('amount'), 
                    date=resource.get('date'),
                ))
                total_price += resource.get('amount')
            created_orders = Order.objects.bulk_create(orders)
            party = Party.objects.create(
                mediator=validated_data.get('user'),
                delivery_date=validated_data.get('delivery_date'),
                payment_date=validated_data.get('payment_date'),
                comment=validated_data.get('comment'),
                audit=validated_data.get('audit'),
                audit_comment=validated_data.get('audit_comment')
            )
            party.orders.add(*created_orders)
            party.save()
            PartyAmount.objects.create(
                total_price=total_price,
                party=party,
            )
            return party