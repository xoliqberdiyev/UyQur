from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics, views

from core.apps.products.serializers.folder import FolderSerializer, SubFolderSerializer
from core.apps.products.models.folder import Folder, SubFolder
from core.apps.accounts.permissions.permissions import HasRolePermission


class FolderCreateApiView(generics.CreateAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']


class FolderListApiView(generics.ListAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']
    pagination_class = None


class FolderUdateApiView(generics.UpdateAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']
    lookup_field = 'id'



class FolderDeleteApiView(generics.DestroyAPIView):
    serializer_class = FolderSerializer
    queryset = Folder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']
    lookup_field = 'id'


class SubFolderCreateApiView(generics.CreateAPIView):
    serializer_class = SubFolderSerializer
    queryset = SubFolder.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']
    lookup_field = 'id'


class SubFolderListByFolderIdApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']

    def get(self, request, folder_id):
        folder = get_object_or_404(Folder, id=folder_id)
        sub_folders = SubFolder.objects.filter(folder=folder)
        serializer = SubFolderSerializer(sub_folders, many=True)
        return Response(serializer.data, status=200)


class SubFolderUpdateApiView(generics.UpdateAPIView):
    serializer_class = SubFolderSerializer
    queryset = SubFolder.objects.all()
    lookup_field = 'id'
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']


class SubFolderDeleteApiView(generics.DestroyAPIView):
    serializer_class = SubFolderSerializer
    queryset = SubFolder.objects.all()
    lookup_field = 'id'
    permission_classes = [HasRolePermission]
    required_permissions = ['product_folder']

