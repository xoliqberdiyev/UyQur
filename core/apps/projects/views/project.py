from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from rest_framework import generics, status, views
from rest_framework.response import Response

from core.apps.projects.models.project import Project, ProjectFolder
from core.apps.projects.serializers import project as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class ProjectListApiView(generics.ListAPIView):
    serializer_class = serializers.ProjectListSerializer
    queryset = Project.objects.filter(is_archive=False).select_related('location')
    permission_classes = [HasRolePermission]
    required_permissions = ['project']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Project.objects.exclude(folder__isnull=False)


class ProjectDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.ProjectDetailSerialzier
    queryset = Project.objects.select_related('location')
    permission_classes = [HasRolePermission]
    required_permissions = ['project']
    lookup_field = 'id'


class ProjectCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.ProjectCreateSerializer
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project']


class ProjectUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.ProjectUpdateSerialzier
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project']
    lookup_field = 'id'


class ProjectDeleteApiView(generics.DestroyAPIView):
    permission_classes = [HasRolePermission]
    lookup_field = 'id'
    required_permissions = ['project']
    queryset = Project.objects.all()


class ArchiveProjectApiView(generics.GenericAPIView):
    serializer_class = None
    permission_classes = [HasRolePermission]
    required_permissions = ['project']

    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        project.is_archive = True
        project.save()
        return Response({"success": True, "message": "Archived"}, status=200)


# Project Folder
class ProjectFolderCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.ProjectFolderCreateSerializer
    queryset = ProjectFolder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project_folder']


class ProjectFolderListApiView(generics.ListAPIView):
    serializer_class = serializers.ProjectFolderListSerializer
    queryset = ProjectFolder.objects.prefetch_related(
        Prefetch('projects', Project.objects.filter(is_archive=False))
    )
    permission_classes = [HasRolePermission]
    required_permissions = ['project_folder']
    pagination_class = CustomPageNumberPagination


class ProjectFolderCreateProjectApiView(generics.CreateAPIView):
    serializer_class = serializers.ProjectFolderProjectCreateSerializer
    queryset = Project.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project_folder']


class ProjectFolderUpdateApiView(generics.GenericAPIView):
    serializer_class = serializers.ProjectFolderUpdateSerializer
    queryset = ProjectFolder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['project_folder']

    def put(self, request, id):
        folder = get_object_or_404(ProjectFolder, id=id)
        serializer = self.serializer_class(data=request.data, instance=folder)
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True, 'message': "Folder updated!"}, status=200)
        return Response({"success": False, 'message': serializer.errors}, status=400)
    

class ProjectFolderDetailApiView(generics.GenericAPIView):
    serializer_class = serializers.ProjectFolderDetailSerializer
    queryset = ProjectFolder.objects.select_related('projects')
    permission_classes = [HasRolePermission]
    required_permissions = ['project_folder']

    def get(self, request, id):
        folder = get_object_or_404(ProjectFolder, id=id)
        serializer = self.serializer_class(folder)
        return Response(serializer.data, status=200)
    

class ProjectFolderDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['project_folder']

    def delete(self, request, id):
        folder = get_object_or_404(ProjectFolder, id=id)
        folder.delete()
        return Response({"success": True, "message": 'deleted!'}, status=204)
    

class ChangeProjectFolderApiView(generics.GenericAPIView):
    serializer_class = serializers.ChangeProjectFolderSerializer
    queryset = Project.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            project = serializer.validated_data.get('project')
            folder = serializer.validated_data.get('project_folder')
            project.folder = folder
            project.save()
            return Response(
                {'success': True, 'message': 'Project Folder changed!'},
                status=200
            )
        return Response(
            {'success': False, 'message': serializer.errors}, status=400
        )