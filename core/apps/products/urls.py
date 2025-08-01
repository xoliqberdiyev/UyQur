from django.urls import path, include

from core.apps.products.views import product as product_views

urlpatterns = [
    path('product/', include(
        [
            path('list/', product_views.ProductListApiView.as_view()),
        ]
    ))
]