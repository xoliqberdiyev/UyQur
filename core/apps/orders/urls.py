from django.urls import path, include

from core.apps.orders.views import order_application as application_views
from core.apps.orders.views import order as order_views


urlpatterns = [
    path('order_application/', include(
        [
            path('create/', application_views.OrderApplicationCreateApiView.as_view()),
            path('list/', application_views.OrderApplicationListApiView.as_view()),
        ]
    )),
    path('order/', include(
        [
            path('list/', order_views.OrderListApiView.as_view()),
        ]
    )),
]