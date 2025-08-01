from rest_framework import serializers

from core.apps.projects.models.project import Project, ProjectDepartment


class ProjectDepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDepartment
        fields = [
            'id', 'name'
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date'
        ]


class ProjectDetailSerialzier(serializers.ModelSerializer):
    project_departments = ProjectDepartmentListSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'location', 'start_date', 'end_date', 'project_departments'
        ]