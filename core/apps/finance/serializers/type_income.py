from rest_framework import serializers

from core.apps.finance.models import TypeIncome


class TypeIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeIncome
        fields = [
            'id', 'name', 'category', 'activity', 'comment', 'status'
        ]