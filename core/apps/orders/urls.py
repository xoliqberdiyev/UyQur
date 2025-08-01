from django.urls import path, include

from core.apps.orders.views import order as order_views

urlpatterns = [
    path('order_application/', include(
        [
            path('create/', order_views.OrderApplicationCreateApiView.as_view()),
        ]
    )),
]