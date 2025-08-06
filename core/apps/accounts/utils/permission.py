def get_permissions_with_tabs(user):
    if not user.role:
        return {}

    permissions = user.role.permissions.all()

    result = {}
    for perm in permissions:
        tab_codes = list(perm.permission_tab.values_list('code', flat=True))
        result[perm.code] = tab_codes

    return result