from rest_framework import serializers

from core.apps.accounts.models.permission import PermissionToTab, PermissionToAction, Permission


class PermissionToActionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionToAction
        fields = [
            'id', 'name', 'code'
        ]


class PermissionToTabListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionToTab
        fields = [
            'id', 'name', 'code'
        ]


class PermissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'code'
        ]