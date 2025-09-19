from rest_framework import serializers

from core.apps.accounts.models.role import Role


class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'comment']

    
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'name', 'comment', 'permissions', 'permission_to_tabs', 'permission_to_actions'
        ]