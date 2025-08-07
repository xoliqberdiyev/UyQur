from rest_framework import serializers

from core.apps.shared.models import Region, District


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name']


class RegionListSerializer(serializers.ModelSerializer):
    districts = DistrictListSerializer(many=True)
    
    class Meta:
        model = Region
        fields = [
            'id', 'name', 'districts'
        ]