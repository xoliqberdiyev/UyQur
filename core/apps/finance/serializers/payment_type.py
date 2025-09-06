from rest_framework import serializers

from core.apps.finance.models import PaymentType


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = [
            'id', 'name'
        ]
        