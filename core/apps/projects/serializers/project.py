from django.db import transaction

from rest_framework import serializers

from core.apps.projects.models.project import Project, ProjectFolder


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date'
        ]


class ProjectDetailSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date',
        ]


class ProjectCreateSerializer(serializers.Serializer):
    location = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            return Project.objects.create(
                name=validated_data.get('name'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                location=validated_data.get('location')
            )


class ProjectFolderCreateSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        with transaction.atomic():
            folder = ProjectFolder.objects.create(
                name=validated_data.get('name')
            )
            return folder


class ProjectFolderListSerializer(serializers.ModelSerializer):
    projects = ProjectListSerializer(many=True)

    class Meta:
        model = ProjectFolder
        fields = ['id', 'name', 'projects']


class ProjectFolderProjectCreateSerializer(serializers.Serializer):
    folder_id = serializers.UUIDField()
    name = serializers.CharField()
    location = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        folder = ProjectFolder.objects.filter(id=data['folder_id']).first()
        if not folder:
            raise serializers.ValidationError("Folder not found")
        data['folder'] = folder
        return data 
    
    def create(self, validated_data):
        with transaction.atomic():
            return Project.objects.create(
                name=validated_data.get('name'),
                folder=validated_data.get('folder'),
                location=validated_data.get('location'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date')
            )
        
