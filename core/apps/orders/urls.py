from django.urls import path, include

from core.apps.orders.views import order as order_views


urlpatterns = [
    path('order/', include(
        [
            path('list/', order_views.OrderListApiView.as_view()),
            path('create/', order_views.OrderCreateApiView.as_view()),
        ]
    )),
]