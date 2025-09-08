from rest_framework import serializers

from core.apps.finance.models import ExpenceType


class ExpenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenceType
        fields = [
            'id', 'name'
        ]