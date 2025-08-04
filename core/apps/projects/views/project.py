from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.projects.models.project import Project, ProjectDepartment, ProjectFolder
from core.apps.projects.serializers import project as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class ProjectListApiView(generics.ListAPIView):
    serializer_class = serializers.ProjectListSerializer
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination


class ProjectDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.ProjectDetailSerialzier
    queryset = Project.objects.prefetch_related('project_departments')
    permission_classes = [HasRolePermission]
    required_permissions = []
    lookup_field = 'id'


class ProjectCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.ProjectCreateSerializer
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []


# Project Folder
class ProjectFolderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.ProjectFolderCreateSerializer
    queryset = ProjectFolder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []


class ProjectFolderListApiView(generics.ListAPIView):
    serializer_class = serializers.ProjectFolderListSerializer
    queryset = ProjectFolder.objects.prefetch_related('projects')
    permission_classes = [HasRolePermission]
    required_permissions = []
    pagination_class = CustomPageNumberPagination


class ProjectFolderCreateProjectApiView(generics.CreateAPIView):
    serializer_class = serializers.ProjectFolderProjectCreateSerializer
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []