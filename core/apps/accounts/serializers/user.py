from rest_framework import serializers

from core.apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(method_name='get_permissions')

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'username', 'role', 'profile_image', 'permissions'
        ]
        extra_kwargs = {'role': {'read_only': True}, "permissions": {'read_only': True}}

    def get_permissions(self, obj):
        if obj.role:
            return obj.role.permissions.values_list('code', flat=True)
        else:
            return None
        
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('first_name', instance.username)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance