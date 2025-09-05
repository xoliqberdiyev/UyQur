from django.db import transaction

from rest_framework import serializers

from core.apps.finance.models import CashTransaction, CashTransactionFolder
from core.apps.accounts.models import User
from core.apps.finance.models import PaymentType


class CashTransactionEmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = [
            'id', 'profile_image', 'first_name', 'last_name', 'username'
        ]


class CashTransactionListSerializer(serializers.ModelSerializer):
    payment_type = serializers.SerializerMethodField(method_name='get_payment_type')
    employees = CashTransactionEmployeeListSerializer(many=True)

    class Meta:
        model = CashTransaction
        fields = [
            'id', 'name', 'payment_type', 'employees', 'status'
        ]

    def get_payment_type(self, obj):
        return {
            "id": obj.payment_type.id,
            "name": obj.payment_type.name
        }
    

class CashTransactionCreateSerializer(serializers.Serializer):
    payment_type_id = serializers.UUIDField()
    employee_ids = serializers.ListSerializer(child=serializers.UUIDField())
    name = serializers.CharField()
    status = serializers.BooleanField()
    folder_id = serializers.UUIDField(required=False)

    def validate(self, data):
        payment_type = PaymentType.objects.filter(id=data['id']).first()
        if payment_type:
            raise serializers.ValidationError("Payment Type not found")
        if data.get('folder_id'):
            folder = CashTransactionFolder.objects.filter(id=data.get('folder_id')).first()
            if not folder:
                raise serializers.ValidationError("Cash Transaction Folder not found")
            data['folder'] = folder
        data['payment_type'] = payment_type
        return data

    def create(self, validated_data):
        with transaction.atomic():
            employee_ids = validated_data.pop('employee_ids')
            cash_transaction = CashTransaction.objects.create(
                name=validated_data.get('name'),
                payment_type=validated_data.get('payment_type'),
                status=validated_data.get('status'),
                folder=validated_data.get('folder')
            )
            cash_transaction.employees.set(employee_ids)
            cash_transaction.save()
            return cash_transaction
    