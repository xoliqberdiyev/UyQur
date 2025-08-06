from rest_framework import serializers

from core.apps.accounts.models.role import Role


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']