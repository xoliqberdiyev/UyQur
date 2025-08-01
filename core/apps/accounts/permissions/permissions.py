from rest_framework.permissions import BasePermission

class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        required_permissions = getattr(view, 'required_permissions', [])
        if not required_permissions:
            return True 

        if user.role:
            user_permissions = user.role.permissions.values_list('code', flat=True)
            return all(perm in user_permissions for perm in required_permissions)

        return False