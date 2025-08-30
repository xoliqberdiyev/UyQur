from django.db import transaction

from rest_framework import serializers

from core.apps.counterparty.models import Counterparty, CounterpartyFolder
from core.apps.shared.models import Region, District


class CounterpartyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = [
            'id', 'inn', 'name', 'phone', 'type', 'folder', 'type', 'region', 'district',
            'balance', 'balance_currency', 'balance_date', 'comment',
        ]
    

class CounterpartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counterparty
        fields = [
            'id', 'name'
        ]

    
class CounterpartyCreateSerializer(serializers.Serializer):
    inn = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()
    type = serializers.ChoiceField(choices=Counterparty.TYPE, required=False)
    folder_id = serializers.UUIDField(required=False)
    region_id = serializers.UUIDField(required=False)
    district_id = serializers.UUIDField(required=False)
    balance = serializers.IntegerField(required=False)
    balance_date = serializers.DateField(required=False)
    comment = serializers.CharField(required=False)

    def validate(self, data):
        if data.get('folder_id'):
            folder = CounterpartyFolder.objects.filter(id=data.get('folder_id')).first()
            if not folder:
                raise serializers.ValidationError("Counterparty Folder not found")
            data['folder'] = folder
        if data.get('region_id'):
            region = Region.objects.filter(id=data.get('region_id')).first()
            if not region:
                raise serializers.ValidationError("Region not found")
            data['region'] = region
        if data.get('district_id'):
            district = District.objects.filter(id=data.get('district_id')).first()
            if not district:
                raise serializers.ValidationError("District not found")
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            return Counterparty.objects.create(
                inn=validated_data.get('inn'),
                name=validated_data.get('name'),
                phone=validated_data.get('phone'),
                type=validated_data.get('type'),
                folder=validated_data.get('folder'),
                region=validated_data.get('region'),
                district=validated_data.get('district'),
                balance=validated_data.get('balance'),
                balance_date=validated_data.get('balance_date'),
                comment=validated_data.get('comment'),
            )
