import django_filters

from core.apps.finance.models import Income


class IncomeFilter(django_filters.FilterSet):
    class Meta:
        model = Income
        fields = [
            'payment_type', 'project_folder', 'project', 'user', 'type_income'
        ]