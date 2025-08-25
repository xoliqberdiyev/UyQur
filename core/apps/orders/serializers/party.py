from django.db import transaction

from rest_framework import serializers

from core.apps.orders.models import Party, PartyAmount, Order, DeletedParty
from core.apps.orders.serializers.order import MultipleOrderAddSerializer, OrderListSerializer
from core.apps.accounts.models import User
from core.apps.counterparty.serializers.counterparty import CounterpartyListPartySerializer
from core.apps.orders.tasks.order import create_inventory
from core.apps.shared.models import UsdCourse
from core.apps.products.models import Product, Unity
from core.apps.projects.models import Project, ProjectFolder
from core.apps.wherehouse.models import WhereHouse
from core.apps.counterparty.models import Counterparty


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
    currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')])

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
                create_inventory.delay(resource['wherehouse_id'], resource['quantity'], resource['product_id'], resource['unity_id'], resource['total_price'])
                if validated_data.get('currency') == 'uzs':
                    if resource.get('currency') == 'usd':
                        usd_value = UsdCourse.objects.first().value
                        total_price += resource.get('amount') * usd_value
                else:
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
                currency=validated_data.get('currency'),
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
    mediator = serializers.SerializerMethodField(method_name='get_mediator')

    class Meta:
        model = Party
        fields = [
            'id', 'number', 'delivery_date', 'closed_date', 'order_date', 'payment_date', 'status',
            'payment_status', 'process', 'confirmation', 'comment', 'audit', 'audit_comment',
            'orders', 'party_amount', 'mediator', 'currency'
        ]

    def get_mediator(self, obj):
        return {
            'id': obj.mediator.id,
            'full_name': obj.mediator.full_name
        }


class PartyListSerializer(serializers.ModelSerializer):
    party_amount = PartyAmountSerializer()
    mediator = serializers.SerializerMethodField(method_name='get_mediator')
    counterparty = serializers.SerializerMethodField(method_name='get_counterparty')

    class Meta:
        model = Party
        fields = [
            'id','number', 'delivery_date', 'closed_date', 'order_date', 'payment_date', 'status',
            'payment_status', 'process', 'confirmation', 'comment', 'audit', 'audit_comment',
            'party_amount', 'mediator', 'counterparty', 'currency'
        ]

    def get_mediator(self, obj):
        return {
            'id': obj.mediator.id,
            'full_name': obj.mediator.full_name
        }

    def get_counterparty(self, obj):
        counterparties = obj.orders.values("counterparty__id", "counterparty__name").distinct()
        counterparties = [
            {"id": c["counterparty__id"], "name": c["counterparty__name"]}
            for c in counterparties
        ]
        return CounterpartyListPartySerializer(counterparties, many=True).data


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


class PartyOrderUpdateSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    product_id = serializers.UUIDField()
    unity_id = serializers.UUIDField()
    project_folder_id = serializers.UUIDField(required=False)
    project_id = serializers.UUIDField(required=False)
    wherehouse_id = serializers.UUIDField()
    counterparty_id = serializers.UUIDField()
    quantity = serializers.IntegerField()
    unit_amount = serializers.IntegerField()
    currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')])
    total_price = serializers.IntegerField()

    def validate(self, data):
        order = Order.objects.filter(id=data['order_id']).first()
        if not order:
            raise serializers.ValidationError("Order not found")
        product = Product.objects.filter(id=data['product_id']).first()
        if not product:
            raise serializers.ValidationError(f"Product not found on {order.id}")
        unity = Unity.objects.filter(id=data['unity_id']).first()
        if not unity:
            raise serializers.ValidationError(f"Unity not found on {order.id}")
        if data.get('project_folder_id'):
            project_folder = ProjectFolder.objects.filter(id=data['project_folder_id']).first()
            if not project_folder:
                raise serializers.ValidationError(f"Project Folder not found on {order.id}")
            data['project_folder'] = project_folder
        if data.get('project_id'):
            project = Project.objects.filter(id=data['project_id']).first()
            if not project:
                raise serializers.ValidationError(f"Project not found on {order.id}")
            data['project'] = project
        wherehouse = WhereHouse.objects.filter(id=data['wherehouse_id']).first()
        if not wherehouse:
            raise serializers.ValidationError(f"WhereHouse not found on {order.id}")
        counterparty = Counterparty.objects.filter(id=data['counterparty_id']).first()
        if not counterparty:
            raise serializers.ValidationError(f"Counterparty not found on {order.id}")

        data['order'] = order
        data['product'] = product
        data['unity'] = unity
        data['wherehouse'] = wherehouse
        data['counterparty'] = counterparty
        return data


class PartyUpdateSerializer(serializers.ModelSerializer):
    orders = PartyOrderUpdateSerializer(many=True, required=False)

    class Meta:
        model = Party
        fields = [
            'mediator', 'delivery_date', 'payment_date', 'orders', 'comment', 'audit', 'audit_comment',
            'discount', 'discount_currency',
        ]
        extra_kwargs = {
            'mediator': {'required': False},
            'delivery_date': {'required': False},
            'payment_date': {'required':False},
            'comment': {'required': False},
            'audit': {'required': False},
            'audit_comment': {'required': False},
            'discount': {'required': False},
            'discount_currency': {'required': False},
        }

    def update(self, instance, validated_data):
        orders_data = validated_data.pop('orders')
        update_orders = []
        with transaction.atomic():
            instance.mediator = validated_data.get('mediator', instance.mediator)
            instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
            instance.payment_date = validated_data.get('payment_date', instance.payment_date)
            instance.save()

            for order_data in orders_data:
                order = order_data['order']
                order.product = order_data['product']
                order.unity = order_data['unity']
                order.wherehouse = order_data['wherehouse']
                order.counterparty = order_data['counterparty']
                order.quantity = order_data['quantity']
                order.currency = order_data['currency']
                order.unit_amount = order_data['unit_amount']
                order.total_price = order_data['total_price']
                if 'project_folder' in order_data:
                    order.project_folder = order_data['project_folder']
                if 'project' in order_data:
                    order.project = order_data['project']

                update_orders.append(order)

            Order.objects.bulk_update(
                update_orders,
                fields=[
                    'product',
                    'unity',
                    'wherehouse',
                    'counterparty',
                    'quantity',
                    'unit_amount',
                    'currency',
                    'total_price',
                    'project_folder',
                    'project'
                ]
            )
            return instance
