from django.urls import path, include

from core.apps.wherehouse.views import wherehouse as wherehouse_views
from core.apps.wherehouse.views import inventory as inventory_views
from core.apps.wherehouse.views import invalid_product as invalid_product_views
from core.apps.wherehouse.views import stock_movemend as stock_movemend_views


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
    path('stock_movemend/', include(
        [
            path('create/', stock_movemend_views.StockMovemendCreateApiView.as_view()),
            path('list/', stock_movemend_views.StockMovemendListApiView.as_view()),
            path('<uuid:id>/delete/', stock_movemend_views.StockMovemendDeleteApiView.as_view()),
        ]
    ))
] 
