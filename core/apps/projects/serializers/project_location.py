from rest_framework import serializers

from core.apps.shared.models import Region, District
from core.apps.projects.models import ProjectLocation


class ProjectLocationSerializer(serializers.Serializer):
    address = serializers.CharField()
    region_id = serializers.UUIDField()
    district_id = serializers.UUIDField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def validate(self, data):
        if data.get('region_id'):
            region = Region.objects.filter(id=data.get('region_id')).first()
            if not region:
                raise serializers.ValidationError("Region not found")
            data['region'] = region
        if data.get('district_id'):
            district = District.objects.filter(id=data['district_id']).first()
            if not district:
                raise serializers.ValidationError("District not found")
            data['district'] = district
        return data


class ProjectLocationListSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField(method_name='get_region')
    district = serializers.SerializerMethodField(method_name='get_district')

    class Meta:
        model = ProjectLocation
        fields = [
            'id', 'address', 'latitude', 'longitude', 'region', 'district'
        ]

    def get_region(self, obj):
        return {
            'id': obj.region.id,
            'name': obj.region.name
        }


    def get_district(self, obj):
        return {
            'id': obj.district.id,
            'name': obj.district.name
        }