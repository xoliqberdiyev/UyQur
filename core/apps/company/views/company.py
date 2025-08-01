from rest_framework import generics, status
from rest_framework.response import Response

from core.apps.company.models import Company
from core.apps.company.serializers import company as serializers

from core.apps.accounts.permissions.permissions import HasRolePermission


class CompanyListApiView(generics.ListAPIView):
    serializer_class = serializers.CompanyListSerializer
    queryset = Company.objects.all()
    permission_classes = [HasRolePermission]
    required_permissions = []


class CompanyDetailApiView(generics.RetrieveAPIView):
    serializer_class = serializers.CompanyDetailSerializer
    queryset = Company.objects.prefetch_related('branches')
    permission_classes = [HasRolePermission]
    required_permissions = []
    lookup_field = 'id'