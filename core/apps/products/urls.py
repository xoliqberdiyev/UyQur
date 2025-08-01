from django.urls import path, include

from core.apps.products.views import product as product_views
from core.apps.products.views import unity as unity_views


urlpatterns = [
    path('product/', include(
        [
            path('list/', product_views.ProductListApiView.as_view()),
        ]
    )),
    path('unity/', include(
        [
            path('list/', unity_views.UnityListApiView.as_view()),
        ]
    )),
]