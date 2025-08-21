import django_filters

from core.apps.orders.models import Order, Offer


class OfferFilter(django_filters.FilterSet):
    class Meta:
        model = Offer
        fields = [
            'order__wherehouse', 'order__project', 'order__project_folder', 'order__date'
        ]