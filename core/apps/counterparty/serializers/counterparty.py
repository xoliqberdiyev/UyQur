from rest_framework import serializers

from core.apps.accounts.serializers.user import UserListSerializer
from core.apps.counterparty.models import Counterparty


class CounterpartySerializer(serializers.ModelSerializer):
    person = UserListSerializer()
    
    class Meta:
        model = Counterparty
        fields = [
            'id', 'name', 'type', 'status', 'description', 'start_date', 'person'
        ]


class CounterpartyListPartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = [
            'id', 'name',
        ]