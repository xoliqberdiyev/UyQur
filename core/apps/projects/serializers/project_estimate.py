from django.db import transaction

from rest_framework import serializers

from core.apps.projects.models.project_estimate import EstimateProduct, EstimateWork, ProjectEstimate


class ProjectEstimateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEstimate
        fields = [
            'id', 'number', 'name'
        ]


class ProjectEstimateCreateSerializer(serializers.Serializer):
    number = serializers.IntegerField()
    name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            return ProjectEstimate.objects.create(
                number=validated_data.get('number'),
                name=validated_data.get('name'),
            )
    
class ProjectEstimateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEstimate
        fields = ['name']
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance