from rest_framework import serializers

from core.apps.finance.models import CashTransactionFolder


class CashTransactionFolderSerializer(serializers.ModelSerializer):
    cash_transaction_count = serializers.SerializerMethodField(method_name='get_cash_transaction_count')

    class Meta:
        model = CashTransactionFolder
        fields = [
            'id', 'name', 'cash_transaction_count'
        ]
        extra_kwargs = {
            'id': {"read_only": True},
            'cash_transaction_count': {"read_only": True},
        }

    def get_cash_transaction_count(self, obj):
        return obj.cash_transactions.count()
