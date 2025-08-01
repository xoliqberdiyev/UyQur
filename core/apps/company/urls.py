from django.urls import path, include 

from core.apps.company.views import company as company_views

urlpatterns = [
    path('company/', include(
        [
            path('list/', company_views.CompanyListApiView.as_view(), name='company-list'),
            path('<uuid:id>/', company_views.CompanyDetailApiView.as_view()),
        ]
    )),
]