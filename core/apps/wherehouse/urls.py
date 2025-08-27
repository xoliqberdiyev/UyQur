from django.urls import path, include

from core.apps.wherehouse.views import wherehouse as wherehouse_views
from core.apps.wherehouse.views import inventory as inventory_views
from core.apps.wherehouse.views import invalid_product as invalid_product_views


urlpatterns = [
    path('warehouse/', include(
        [
            path('list/', wherehouse_views.WhereHouseListApiView.as_view()),
            path('<uuid:id>/', wherehouse_views.WhereHouseDetailApiView.as_view()),
            path('create/', wherehouse_views.WhereHouseCreateApiView.as_view()),
            path('<uuid:id>/delete/', wherehouse_views.WhereHouseDeleteApiView.as_view()),
            path('<uuid:id>/update/', wherehouse_views.WhereHouseUpdateApiView.as_view()),
        ]
    )),
    path('inventory/', include(
        [
            path('list/', inventory_views.InventoryListApiView.as_view()),
        ]
    )),
    path('invalid_product/', include(
        [
            path('create/', invalid_product_views.InvalidProductCreateApiView.as_view()),
            path('list/', invalid_product_views.InvalidProductListApiView.as_view()),
            path('<uuid:id>/update/', invalid_product_views.InvalidProductUpdateApiView.as_view()),
            path('<uuid:id>/delete/', invalid_product_views.InvalidProductDeleteApiView.as_view()),
        ]
    )),
] 
