from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import generics, views, filters

from core.apps.products.serializers.folder import FolderSerializer, SubFolderSerializer
from core.apps.products.models import Folder, SubFolder, Product
from core.apps.products.serializers.product import ProductListSerializer 
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


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


class FolderProductListApiView(generics.GenericAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [HasRolePermission]
    required_permissions = ['product', 'product_folder']
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', 'type', 'unity__value'
    ]

    def get(self, request, folder_id):
        folder = get_object_or_404(Folder, id=folder_id)
        products = self.filter_queryset(Product.objects.filter(folder=folder))
        data = self.paginate_queryset(products)
        serializer = self.serializer_class(data, many=True)
        return self.get_paginated_response(serializer.data)
    

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


class SubFolderProductListApiView(generics.GenericAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [HasRolePermission]
    required_permissions = ['product', 'product_folder']
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get(self, request, sub_folder_id):
        sub_folder = get_object_or_404(SubFolder, id=sub_folder_id)
        products = Product.objects.filter(sub_folder=sub_folder)
        data = self.paginate_queryset(products)
        serializer = self.serializer_class(data, many=True)
        return self.get_paginated_response(serializer.data)
    