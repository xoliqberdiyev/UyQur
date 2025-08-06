from django.urls import path, include 

from core.apps.accounts.views.login import LoginApiView
from core.apps.accounts.views import user as user_views
from core.apps.accounts.views import role as role_views
from core.apps.accounts.views import permission as permission_views


urlpatterns = [
    path('auth/login/', LoginApiView.as_view(), name='login'),
    path('user_profile/', include(
        [
            path('profile/', user_views.UserProfileApiView.as_view()),
            path('profile/update/', user_views.UserProfileUpdateApiView.as_view()),
        ]
    )),
    path('user/', include(
        [
            path('<uuid:id>/delete/', user_views.UserDeleteApiView.as_view()),
            path('create/', user_views.UserCreateApiView.as_view()),
            path('list/', user_views.UserListApiView.as_view()),
            path('<uuid:id>/', user_views.UserUpdateApiView.as_view()),
            path('permissions/', user_views.UserPermissionListApiView.as_view()),
        ]
    )),
    path('role/', include(
        [
            path('list/', role_views.RoleListApiView.as_view()),
        ]
    )),
    path('permission/', include(
        [
            path('list/', permission_views.PermissionListApiView.as_view()),
        ]
    )),
]