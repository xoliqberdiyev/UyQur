from django.urls import path, include

from core.apps.orders.views import order as order_views
from core.apps.orders.views import offer as offer_views
from core.apps.orders.views import party as party_views


urlpatterns = [
    path('order/', include(        [
            path('list/', order_views.OrderListApiView.as_view()),
            path('create/', order_views.OrderCreateApiView.as_view()),
            path('<uuid:id>/update/', order_views.OrderUpdateApiView.as_view()),
            path('<uuid:id>/delete/', order_views.OrderDeleteApiView.as_view()),
            path('<uuid:order_id>/cancel/', order_views.OrderChangeStatusCancelledApiView.as_view()),
            path("<uuid:order_id>/accept/", order_views.OrderChangeStatusAcceptedApiView.as_view()),
            path("accepted/list/", order_views.OrderAcceptApiView.as_view()),
            path('<uuid:order_id>/offers/', order_views.OrderOfferListApiView.as_view()),
        ]
    )),
    path('offer/', include(
        [
            path('create/', offer_views.OffersCreateApiView.as_view()),
            path('list/', offer_views.OfferListApiView.as_view()),
            path('<uuid:id>/delete/', offer_views.OfferDeleteApiView.as_view()),
            path('<uuid:id>/update/', offer_views.OfferUpdateApiView.as_view()),
        ]
    )),
    path('party/', include(
        [
            path('create/', party_views.PartyCreateApiView.as_view()),
        ]
    )),
]