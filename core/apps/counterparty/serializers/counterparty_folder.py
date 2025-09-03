from django.db import transaction

from rest_framework import serializers

from core.apps.counterparty.models import CounterpartyFolder


class CounterpartyFolderListSerializer(serializers.ModelSerializer):
    counterparty_count = serializers.SerializerMethodField(method_name='get_counterparty_count')

    class Meta:
        model = CounterpartyFolder
        fields = [
            'id', 'name', 'counterparty_count'
        ]

    def get_counterparty_count(self, obj):
        return obj.counterparties.count()


class CounterpartyFolderCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            return CounterpartyFolder.objects.create(
                name=validated_data.get('name'),
            )