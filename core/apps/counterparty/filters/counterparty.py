import django_filters

from core.apps.counterparty.models import Counterparty


class CounterpartyFilter(django_filters.FilterSet):
    class Meta:
        model = Counterparty
        fields = [
            'type', 'status'
        ]