from django.shortcuts import get_object_or_404

from rest_framework import generics, views
from rest_framework.response import Response

from core.apps.shared.serializers.region import RegionListSerializer, DistrictListSerializer
from core.apps.shared.models import Region, District
from core.apps.accounts.permissions.permissions import HasRolePermission



class RegionListApiView(generics.ListAPIView):
    permission_classes = [HasRolePermission]
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer
    required_permissions = ['project', 'project_folder']
    pagination_class = None


class DistrictListApiView(views.APIView):
    permission_classes = [HasRolePermission]
    required_permissions = ['project', 'project_folder']

    def get(self, request, id):
        region = get_object_or_404(Region, id=id)
        districts = District.objects.filter(region=region)
        serializer = DistrictListSerializer(districts, many=True)
        return Response(serializer.data, status=200)