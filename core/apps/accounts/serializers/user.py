from rest_framework import serializers

from core.apps.accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(method_name='get_permissions')

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'username', 'phone_number', 'is_blocked', 'role', 'profile_image', 'permissions'
        ]
        extra_kwargs = {'role': {'read_only': True}, "permissions": {'read_only': True}}

    def get_permissions(self, obj):
        if obj.role:
            return obj.role.permissions.values_list('code', flat=True)
        else:
            return None
        
    def update(self, instance, validated_data):
        instance.role = validated_data.get('role', instance.role)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.save()
        return instance