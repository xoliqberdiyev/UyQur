from django.urls import path, include

from core.apps.projects.views import project as project_views

urlpatterns = [
    path('project/', include(
        [
            path('list/', project_views.ProjectListApiView.as_view()),
            path('<uuid:id>/', project_views.ProjectDetailApiView.as_view()),
        ]
    ))
]