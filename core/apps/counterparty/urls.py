from django.urls import path, include

from core.apps.counterparty.views import counterparty as cp_views
from core.apps.counterparty.views import counterparty_folder as folder_views


urlpatterns = [
    path('counterparty/', include(
        [
            path('list/', cp_views.CounterpartyListApiView.as_view()),
            path('create/', cp_views.CounterpartyCreateApiView.as_view()),
            path('<uuid:id>/archive/', cp_views.ArchiveCounterpartyApiView.as_view()),
            path('archived/list/', cp_views.ArchivedCounterpartyListApiView.as_view()),
            path('<uuid:id>/delete/', cp_views.CounterpartyDeleteApiView.as_view()),
            path('<uuid:id>/update/', cp_views.CounterpartyUpdateApiView.as_view()),
        ]
    )),
    path('counterparty_folder/', include(
        [
            path('list/', folder_views.CounterpartyFolderListApiView.as_view()),
            path('create/', folder_views.CounterpartyCreateApiView.as_view()),
            path('<uuid:id>/delete/', folder_views.CounterpartyDeleteApiView.as_view()),
            path('<uuid:id>/update/', folder_views.CounterpartyUpdateApiView.as_view()),
        ]
    ))
]