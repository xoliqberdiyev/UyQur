from django.urls import path, include

from core.apps.counterparty.views import counterparty as cp_views


urlpatterns = [
    path('counterparty/', include(
        [
            path('list/', cp_views.CounterpartyListApiView.as_view()),
            path('create/', cp_views.CounterpartyCreateApiView.as_view()),
        ]
    ))    
]