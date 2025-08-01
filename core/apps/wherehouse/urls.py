from django.urls import path, include

from core.apps.wherehouse.views import wherehouse as wherehouse_views


urlpatterns = [
    path('wherehouse/', include(
        [
            path('list/', wherehouse_views.WhereHouseListApiView.as_view()),
            path('<uuid:id>/', wherehouse_views.WhereHouseDetailApiView.as_view()),
        ]
    ))
]