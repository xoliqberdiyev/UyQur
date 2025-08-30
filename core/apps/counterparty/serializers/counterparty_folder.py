from django.db import transaction

from rest_framework import serializers

from core.apps.counterparty.models import CounterpartyFolder


class CounterpartyFolderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterpartyFolder
        fields = [
            'id', 'name'
        ]


class CounterpartyFolderCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            return CounterpartyFolder.objects.create(
                name=validated_data.get('name'),
            )