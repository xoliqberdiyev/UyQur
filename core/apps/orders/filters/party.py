from calendar import monthrange

from django.utils.timezone import timedelta, now

import django_filters

from core.apps.orders.models import Party


class PartyFilter(django_filters.FilterSet):
    DATE_CHOICES = (
        ('today', 'bugun'),
        ('last_week', 'oxirgi hafta'),
        ('last_month', 'oxirgi oy'),
        ('last_year', 'oirgi yil'),

    )
    # delivery date filters
    delivery_date = django_filters.ChoiceFilter(
        choices=DATE_CHOICES, method='filter_by_deliveyer_date'
    )
    delivery_start_date = django_filters.DateFilter(field_name="delivery_date", lookup_expr="gte")
    delivery_end_date = django_filters.DateFilter(field_name="delivery_date", lookup_expr="lte")
    # payment date filters
    payment_date = django_filters.ChoiceFilter(
        choices=DATE_CHOICES, method='filter_by_payment_date'
    )
    payment_start_date = django_filters.DateFilter(field_name='payment_date', lookup_expr='gte')
    payment_end_date = django_filters.DateFilter(field_name='payment_date', lookup_expr='lte')
    # order date filters
    order_date = django_filters.ChoiceFilter(
        choices=DATE_CHOICES, method='filter_by_order_date'
    )
    order_start_date = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    order_end_date = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')
    
    class Meta:
        model = Party
        fields = [
            
        ]

    def filter_by_delivery_date(self, queryset, name, value):
        today = now().date()
        
        if value == 'today':
            return queryset.filter(delivery_date=today)
        
        elif value == 'last_week':
            start_date = today - timedelta(days=today.weekday() + 7)
            end_date = start_date + timedelta(days=6)
            return queryset.filter(delivery_date__range=(start_date, end_date))

        elif value == 'last_year':
            if today.month == 1:
                last_month_year = today.year - 1
                last_month = 12
            else:
                last_month_year = today.year
                last_month = today.moth - 1
            
            start_last_month = today.replace(year=last_month_year, month=last_month, day=1)
            days_in_last_month = monthrange(last_month_year, last_month)[1]
            end_last_month = start_last_month.replace(day=days_in_last_month)

            return queryset.filter(delivery_date__range=(start_last_month, end_last_month))

        elif value == 'last_year':
            start_year = today.replace(year=today.year - 1, month=1, day=1)
            end_year = today.replace(year=today.year - 1, month=12, day=31)
            return queryset.filter(delivery_date__range=(start_year, end_year))
        return queryset

    def filter_by_payment_date(self, queryset, name, value):
        today = now().date()

        if value == 'today':
            return queryset.filter(payment_date=today)
        elif value == 'last_week':
            start_date = today - timedelta(days=today.weekday() + 7)
            end_date = start_date + timedelta(days=6)
            return queryset.filter(payment_date__range=(start_date, end_date))
        elif value == 'last_month':
            if today.month == 1:
                last_month_year = today.year - 1
                last_month = 12
            else:
                last_month_year = today.year
                last_month = today.moth - 1
            
            start_last_month = today.replace(year=last_month_year, month=last_month, day=1)
            days_in_last_month = monthrange(last_month_year, last_month)[1]
            end_last_month = start_last_month.replace(day=days_in_last_month)

            return queryset.filter(payment_date__range=(start_last_month, end_last_month))
        elif value == 'last_year':
            start_year = today.replace(year=today.year - 1, month=1, day=1)
            end_year = today.replace(year=today.year - 1, month=12, day=31)
            return queryset.filter(payment_date__range=(start_year, end_year))
        return queryset
    
        
