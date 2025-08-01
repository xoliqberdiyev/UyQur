from rest_framework import serializers

from core.apps.company.models import Company
from core.apps.company.serializers.branch import BranchListSerializer


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']


class CompanyDetailSerializer(serializers.ModelSerializer):
    branches = BranchListSerializer(many=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'branches']