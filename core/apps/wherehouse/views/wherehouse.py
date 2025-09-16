from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.wherehouse.models import WhereHouse, Inventory
from core.apps.wherehouse.serializers import wherehouse as serializers
from core.apps.accounts.permissions.permissions import HasRolePermission


class WhereHouseListApiView(generics.ListAPIView):
    serializer_class = serializers.WhereHouseListSerializer
    queryset = WhereHouse.objects.select_related('branch')
    permission_classes = [HasRolePermission]


class WhereHouseDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.WhereHouseDetailSerializer
    queryset = WhereHouse.objects.select_related('branch')
    permission_classes = [HasRolePermission]
    lookup_field = 'id'


class WhereHouseCreateApiView(generics.CreateAPIView):
    serializer_class = serializers.WhereHouseCreateSerializer
    queryset = WhereHouse.objects.all()
    permission_classes = [HasRolePermission]


class WhereHouseDeleteApiView(views.APIView):
    permission_classes = [HasRolePermission]

    def delete(self, request, id):
        wherehouse = get_object_or_404(WhereHouse, id=id)
        wherehouse.delete()
        return Response(
            {'success': True, 'message': 'Deleted!'},
            status=204
        )


class WhereHouseUpdateApiView(generics.UpdateAPIView):
    serializer_class = serializers.WhereHouseUpdateSerializer
    queryset = WhereHouse.objects.all()
    lookup_field = 'id'
    permission_classes = [HasRolePermission]