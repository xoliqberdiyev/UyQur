from rest_framework import serializers

from core.apps.accounts.models.permission import PermissionToTab, PermissionToAction, Permission


class PermissionToActionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionToAction
        fields = [
            'id', 'name', 'code'
        ]


class PermissionToTabListSerializer(serializers.ModelSerializer):
    permission_to_actions = PermissionToActionListSerializer(many=True) 

    class Meta:
        model = PermissionToTab
        fields = [
            'id', 'name', 'code', 'permission_to_actions'
        ]


class PermissionListSerializer(serializers.ModelSerializer):
    permission_tab = PermissionToTabListSerializer(many=True)

    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'code', 'permission_tab'
        ]