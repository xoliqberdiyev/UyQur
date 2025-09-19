from django.db import transaction

from rest_framework import serializers

from core.apps.accounts.models import User
from core.apps.accounts.models.role import Role


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
    

class UserCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    username = serializers.CharField()
    phone_number = serializers.CharField()
    profile_image = serializers.ImageField(required=False)
    role_id = serializers.UUIDField()
    is_blocked = serializers.BooleanField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        role = Role.objects.filter(id=data['role_id']).first()
        if not role:
            raise serializers.ValidationError("role not found")
        data['role'] = role
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("User with this username already exists")
        return data
    
    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create(
                username=validated_data.get('username'),
                full_name=validated_data.get('full_name'),
                phone_number=validated_data.get('phone_number'),
                profile_image=validated_data.get('profile_image'),
                role=validated_data.get('role'),
                is_blocked=validated_data.get('is_blocked'),
            )
            user.set_password(validated_data.get('password'))
            user.save()
            return user
        

class UserListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(method_name='get_role')
    
    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'profile_image', 'phone_number', 'role', 'username', 'is_blocked'
        ]

    def get_role(self, obj):
        if obj.role:
            return {
                'id': obj.role.id,
                'role': obj.role.name,
            }
        return None
    

class UserUpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def validate(self, data):
        user = self.context.get('user')
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError("Password incorrect")
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Ikkita parol bir xil bolishi kerak")
        return data