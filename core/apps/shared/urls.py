from django.urls import path, include 

from core.apps.shared.views import region as region_views

urlpatterns = [
    path('region/list/', region_views.RegionListApiView.as_view()),
    path('region/<uuid:id>/districts/', region_views.DistrictListApiView.as_view()),
]