from django.urls import path, include

from core.apps.projects.views import project as project_views
from core.apps.projects.views import builder as builder_views
from core.apps.projects.views import project_estimate as estimate_views

urlpatterns = [
    path('project/', include(
        [
            path('list/', project_views.ProjectListApiView.as_view()),
            path('<uuid:id>/', project_views.ProjectDetailApiView.as_view()),
            path('create/', project_views.ProjectCreateApiView.as_view()),
            path('<uuid:id>/update/', project_views.ProjectUpdateApiView.as_view()),
            path('<uuid:id>/delete/', project_views.ProjectDeleteApiView.as_view()),
            path('change_folder/', project_views.ChangeProjectFolderApiView.as_view()),
            path('archive/<uuid:id>/', project_views.ArchiveProjectApiView.as_view()),
        ]
    )),
    path('project_folder/', include(
        [
            path('create/', project_views.ProjectFolderCreateApiView.as_view()),
            path('list/', project_views.ProjectFolderListApiView.as_view()),
            path('create/project/', project_views.ProjectFolderCreateProjectApiView.as_view()),
            path('<uuid:id>/update/', project_views.ProjectFolderUpdateApiView.as_view()),
            path('<uuid:id>/', project_views.ProjectFolderDetailApiView.as_view()),
            path('<uuid:id>/delete/', project_views.ProjectFolderDeleteApiView.as_view()),
        ]
    )),
    path('builder/', include(
        [
            path('list/', builder_views.BuilderListApiView.as_view()),
        ]
    )),
    path('project_estimate/', include(
        [
            path('list/', estimate_views.ProjectEstimateListApiView.as_view()),
            path('create/', estimate_views.ProjectEstimateCreateApiView.as_view()),
            path('<uuid:id>/update/', estimate_views.ProjectEstimateUpdateApiView.as_view()),
            path('<uuid:id>/delete/', estimate_views.ProjectEstimateDeleteApiView.as_view()),
        ]
    ))
]