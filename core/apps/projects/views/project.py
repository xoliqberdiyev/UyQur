from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.projects.models.project import Project, ProjectDepartment
from core.apps.projects.serializers import project as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class ProjectListApiView(generics.ListAPIView):
    serializer_class = serializers.ProjectListSerializer
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []


class ProjectDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.ProjectDetailSerialzier
    queryset = Project.objects.prefetch_related('project_departments')
    permission_classes = [HasRolePermission]
    required_permissions = []
    lookup_field = 'id'