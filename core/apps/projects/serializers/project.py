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
            'id', 'name', 'location', 'start_date', 'end_date', 'status', 'benifit_plan'
        ]


class ProjectCreateSerializer(serializers.Serializer):
    location = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    name = serializers.CharField()

    builder_id = serializers.UUIDField()
    area = serializers.IntegerField()

    boss = serializers.ListSerializer(child=serializers.UUIDField())
    foreman = serializers.ListSerializer(child=serializers.UUIDField())
    other_members = serializers.ListSerializer(child=serializers.UUIDField())

    wherehouse = serializers.ListSerializer(child=serializers.UUIDField())
    cash_transaction = serializers.ListSerializer(child=serializers.UUIDField())
    currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')])
    benifit_plan = serializers.IntegerField()

    def create(self, validated_data):
        boss_ids = validated_data.pop('boss')
        foreman_ids = validated_data.pop('foreman')
        other_member_ids = validated_data.pop('other_members')
        warehouse_ids = validated_data.pop('wherehouse')
        cash_transaction_ids = validated_data.pop('cash_transaction')
        builder_id = validated_data.pop('builder_id')

        with transaction.atomic():
            project = Project.objects.create(
                name=validated_data.get('name'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                location=validated_data.get('location'),
                area=validated_data.get('area'),
                currency=validated_data.get('currency'),
                benifit_plan=validated_data.get('benifit_plan'),
                builder_id=builder_id
            )

            project.boss.set(boss_ids)
            project.foreman.set(foreman_ids)
            project.other_members.set(other_member_ids)
            project.wherehouse.set(warehouse_ids)
            project.cash_transaction.set(cash_transaction_ids)

            return project

# Project Folder
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
        

class ProjectFolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFolder
        fields = [
            'name', 'color'
        ]
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance
    

class ProjectFolderDetailSerializer(serializers.ModelSerializer):
    projects = ProjectListSerializer(many=True)
    projects_count = serializers.SerializerMethodField(method_name='get_projects_count')

    class Meta:
        model = ProjectFolder
        fields = [
            'id', 'name', 'color', 'projects_count', 'projects'
        ]

    def get_projects_count(self, obj):
        return obj.projects.count()
    

class ChangeProjectFolderSerializer(serializers.Serializer):
    project_id = serializers.UUIDField()
    project_folder_id = serializers.UUIDField()

    def validate(self, data):
        project = Project.objects.filter(id=data['project_id']).first()
        if not project:
            raise serializers.ValidationError("Project not found")
        project_folder = ProjectFolder.objects.filter(id=data['project_folder_id']).first()
        if not project_folder:
            raise serializers.ValidationError("Project Folder not found")
        if project.folder == project_folder:
            raise serializers.ValidationError("the project folder is attached for this project")
        data['project'] = project
        data['project_folder'] = project_folder
        return data