from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.products.models import Unity
from core.apps.products.serializers import unity as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.shared.paginations.custom import CustomPageNumberPagination


class UnityListApiView(generics.ListAPIView):
    serializer_class = serializers.UnityListSerializer
    queryset = Unity.objects.all()
    permission_classes = [HasRolePermission]
    pagination_class = CustomPageNumberPagination


class UnityCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.UnityListSerializer
    queryset = Unity.objects.all()
    permission_classes = [HasRolePermission]


class UnityUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.UnityListSerializer
    queryset = Unity.objects.all()
    permission_classes = [HasRolePermission]
    lookup_field = 'id'


class UnityDeleteApiView(generics.DestroyAPIView):
    serializer_class = serializers.UnityListSerializer
    queryset = Unity.objects.all()
    permission_classes = [HasRolePermission]
    lookup_field = 'id'
