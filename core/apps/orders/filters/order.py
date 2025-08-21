import django_filters

from core.apps.orders.models.order import Order


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = [
            'wherehouse', 'project', 'project_folder', 'date'
        ]
    