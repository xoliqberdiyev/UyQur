from django.db import transaction

from rest_framework import serializers

from core.apps.finance.models import CashTransaction, CashTransactionFolder
from core.apps.accounts.models import User
from core.apps.finance.models import PaymentType
from core.apps.finance.serializers.payment_type import PaymentTypeSerializer


class CashTransactionEmployeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = [
            'id', 'profile_image', 'first_name', 'last_name', 'username'
        ]


class CashTransactionListSerializer(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer(many=True)
    employees = CashTransactionEmployeeListSerializer(many=True)

    class Meta:
        model = CashTransaction
        fields = [
            'id', 'name', 'payment_type', 'employees', 'status'
        ]


class CashTransactionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaction
        fields = [
            'name', 'payment_type', 'employees', 'status', 'folder',
        ]


class CashTransactionCreateSerializer(serializers.Serializer):
    payment_type_ids = serializers.ListSerializer(child=serializers.UUIDField(), write_only=True)
    employee_ids = serializers.ListSerializer(child=serializers.UUIDField(), write_only=True)
    name = serializers.CharField()
    status = serializers.BooleanField()
    folder_id = serializers.UUIDField(required=False)

    def validate_name(self, value):
        if CashTransaction.objects.filter(name=value).exists():
            raise serializers.ValidationError('cash transaction with this name already exists')
        return value

    def validate(self, data):
        if data.get('folder_id'):
            folder = CashTransactionFolder.objects.filter(id=data.get('folder_id')).first()
            if not folder:
                raise serializers.ValidationError("Cash Transaction Folder not found")
            data['folder'] = folder
        return data

    def create(self, validated_data):
        with transaction.atomic():
            employee_ids = validated_data.pop('employee_ids', [])
            payment_type_ids = validated_data.pop('payment_type_ids', [])
            cash_transaction = CashTransaction.objects.create(
                name=validated_data.get('name'),
                status=validated_data.get('status'),
                folder=validated_data.get('folder')
            )
            cash_transaction.employees.set(employee_ids)
            cash_transaction.payment_type.set(payment_type_ids)
            cash_transaction.save()
            return cash_transaction
    