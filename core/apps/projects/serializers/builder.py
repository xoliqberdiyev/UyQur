from rest_framework import serializers

from core.apps.projects.models import Builder


class BuilderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = ['id', 'name']