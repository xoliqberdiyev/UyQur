from rest_framework import serializers

from core.apps.projects.models.project_estimate import EstimateProduct, EstimateWork, ProjectEstimate


class ProjectEstimateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEstimate
        fields = [
            'id', 'number', 'name'
        ]
