from django.urls import path, include 

from core.apps.accounts.views.login import LoginApiView
from core.apps.accounts.views.user import UserProfileApiView, UserProfileUpdateApiView, UserDeleteApiView


urlpatterns = [
    path('auth/login/', LoginApiView.as_view(), name='login'),
    path('user/', include(
        [
            path('profile/', UserProfileApiView.as_view()),
            path('profile/update/', UserProfileUpdateApiView.as_view()),
            path('delete/<uuid:id>/', UserDeleteApiView.as_view()),
        ]
    ))
]