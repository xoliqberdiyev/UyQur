import django_filters

from core.apps.wherehouse.models import InvalidProduct


class InvalidProductFilter(django_filters.FilterSet):
    class Meta:
        model = InvalidProduct
        fields = [
            'wherehouse', 'project_folder', 'status', 'invalid_status',
            'witnesses', 'expiry_date'
        ]