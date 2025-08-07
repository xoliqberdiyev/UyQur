from rest_framework import generics

from core.apps.shared.serializers.region import RegionListSerializer
from core.apps.shared.models import Region
from core.apps.accounts.permissions.permissions import HasRolePermission



class RegionListApiView(generics.ListAPIView):
    permission_classes = [HasRolePermission]
    queryset = Region.objects.prefetch_related('districts')
    serializer_class = RegionListSerializer
    required_permissions = ['project', 'project_folder']