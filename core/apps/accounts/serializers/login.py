from rest_framework import serializers

from core.apps.accounts.models.user import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if not user:
            raise serializers.ValidationError("User not found with this credentials")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("User not found with this credentials")
        data['user'] = user
        return data