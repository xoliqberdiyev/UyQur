from django.urls import path, include

from core.apps.orders.views import order as order_views


urlpatterns = [
    path('order/', include(
        [
            path('list/', order_views.OrderListApiView.as_view()),
            path('create/', order_views.OrderCreateApiView.as_view()),
            path('<uuid:id>/update/', order_views.OrderUpdateApiView.as_view()),
            path('<uuid:id>/delete/', order_views.OrderDeleteApiView.as_view()),
        ]
    )),
]