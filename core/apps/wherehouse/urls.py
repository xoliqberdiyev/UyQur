from django.urls import path, include

from core.apps.wherehouse.views import wherehouse as wherehouse_views
from core.apps.wherehouse.views import inventory as inventory_views


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
            path('<uuid:wherehouse_id>/list/', inventory_views.InventoryListApiView.as_view()),
        ]
    )),
]
