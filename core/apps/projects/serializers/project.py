from django.db import transaction

from rest_framework import serializers

from core.apps.projects.models.project import Project, ProjectFolder, ProjectLocation
from core.apps.projects.serializers.project_location import ProjectLocationSerializer, ProjectLocationListSerializer


class ProjectListSerializer(serializers.ModelSerializer):
    location = ProjectLocationListSerializer()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date'
        ]


class ProjectDetailSerialzier(serializers.ModelSerializer):
    location = ProjectLocationListSerializer()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date', 'status', 'benifit_plan'
        ]


class ProjectUpdateSerialzier(serializers.ModelSerializer):
    location = ProjectLocationSerializer()
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date', 'status', 'benifit_plan', 'boss',
            'builder', 'area', 'foreman', 'other_members', 'wherehouse', 'cash_transaction', 'currency',
        ]
    
    
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)

        instance.name = validated_data.get('name', instance.name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.status = validated_data.get('status', instance.status)
        instance.benifit_plan = validated_data.get('benifit_plan', instance.benifit_plan)
        instance.folder = validated_data.get('folder', instance.folder)
        instance.builder = validated_data.get('builder', instance.builder)
        instance.area = validated_data.get('area', instance.area)
        instance.currency = validated_data.get('currency', instance.currency)

        if 'boss' in validated_data:
            instance.boss.set(validated_data['boss'])
        if 'foreman' in validated_data:
            instance.foreman.set(validated_data['foreman'])
        if 'other_members' in validated_data:
            instance.other_members.set(validated_data['other_members'])
        if 'wherehouse' in validated_data:
            instance.wherehouse.set(validated_data['wherehouse'])
        if 'cash_transaction' in validated_data:
            instance.cash_transaction.set(validated_data['cash_transaction'])

        if location_data and instance.location:
            location = instance.location
            location.region = location_data.get('region', location.region)
            location.district = location_data.get('district', location.district)
            location.longitude = location_data.get('longitude', location.longitude)
            location.latitude = location_data.get('latitude', location.latitude)
            location.address = location_data.get('address', location.address)
            location.save()

        instance.save()
        return instance


class ProjectCreateSerializer(serializers.Serializer):
    location = ProjectLocationSerializer()
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
    currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')], required=False)
    benifit_plan = serializers.IntegerField(required=False)

    def create(self, validated_data):
        boss_ids = validated_data.pop('boss')
        foreman_ids = validated_data.pop('foreman')
        other_member_ids = validated_data.pop('other_members')
        warehouse_ids = validated_data.pop('wherehouse')
        cash_transaction_ids = validated_data.pop('cash_transaction')
        builder_id = validated_data.pop('builder_id')

        with transaction.atomic():
            location_data = validated_data.get('location')
            location = ProjectLocation.objects.create(
                address=location_data.get('address'),
                region=location_data.get('region'),
                district=location_data.get('district'),
                latitude=location_data.get('latitude'),
                longitude=location_data.get('longitude'),
            )

            project = Project.objects.create(
                name=validated_data.get('name'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                location=location,
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
    location = ProjectLocationSerializer()
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
    currency = serializers.ChoiceField(choices=[('uzs', 'uzs'), ('usd', 'usd')], required=False)
    benifit_plan = serializers.IntegerField(required=False)

    def validate(self, data):
        folder = ProjectFolder.objects.filter(id=data['folder_id']).first()
        if not folder:
            raise serializers.ValidationError("Folder not found")
        data['folder'] = folder
        return data 
    
    def create(self, validated_data):
        boss_ids = validated_data.pop('boss')
        foreman_ids = validated_data.pop('foreman')
        other_member_ids = validated_data.pop('other_members')
        warehouse_ids = validated_data.pop('wherehouse')
        cash_transaction_ids = validated_data.pop('cash_transaction')
        builder_id = validated_data.pop('builder_id')

        with transaction.atomic():
            location_data = validated_data.get('location')
            location = ProjectLocation.objects.create(
                address=location_data.get('address'),
                region=location_data.get('region'),
                district=location_data.get('district'),
                latitude=location_data.get('latitude'),
                longitude=location_data.get('longitude'),
            )

            project = Project.objects.create(
                name=validated_data.get('name'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                location=location,
                area=validated_data.get('area'),
                currency=validated_data.get('currency'),
                benifit_plan=validated_data.get('benifit_plan'),
                builder_id=builder_id,
                folder=validated_data.get('folder')
            )

            project.boss.set(boss_ids)
            project.foreman.set(foreman_ids)
            project.other_members.set(other_member_ids)
            project.wherehouse.set(warehouse_ids)
            project.cash_transaction.set(cash_transaction_ids)

            return project
        

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