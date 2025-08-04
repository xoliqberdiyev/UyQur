from django.urls import path, include

from core.apps.projects.views import project as project_views

urlpatterns = [
    path('project/', include(
        [
            path('list/', project_views.ProjectListApiView.as_view()),
            path('<uuid:id>/', project_views.ProjectDetailApiView.as_view()),
            path('create/', project_views.ProjectCreateApiView.as_view()),
        ]
    )),
    path('project_folder/', include(
        [
            path('create/', project_views.ProjectFolderCreateApiView.as_view()),
            path('list/', project_views.ProjectFolderListApiView.as_view()),
            path('create/project/', project_views.ProjectFolderCreateProjectApiView.as_view()),
        ]
    ))
]