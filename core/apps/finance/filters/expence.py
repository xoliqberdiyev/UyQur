import django_filters

from core.apps.finance.models import Expence


class ExpenceFilter(django_filters.FilterSet):
    class Meta:
        model = Expence
        fields = [
            'w'
        ]