from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from core.apps.accounts.models.user import User
from core.apps.accounts.serializers.login import LoginSerializer
from core.apps.accounts.permissions.permissions import HasRolePermission
from core.apps.accounts.utils.permission import get_permissions_with_tabs


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')
            token = RefreshToken.for_user(user)
            user_data = {
                'role': user.role.name if user.role else None
            }
            return Response(
                {"access": str(token.access_token), "refresh": str(token), 'user_data': user_data},
                status=status.HTTP_200_OK
            )
