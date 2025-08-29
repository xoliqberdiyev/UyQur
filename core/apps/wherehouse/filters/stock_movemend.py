import django_filters

from core.apps.wherehouse.models.stock_movemend import StockMovemend


class StockMovemendFilter(django_filters.FilterSet):
    class Meta:
        model = StockMovemend
        fields = [
            'wherehouse_to', 'wherehouse_from', 'project_folder', 'project', 'movemend_type', 'date'
        ]