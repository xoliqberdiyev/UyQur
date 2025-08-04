from rest_framework import serializers

from core.apps.finance.models import CashTransaction


class CashTransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaction
        fields = [
            'id', 'name'
        ]