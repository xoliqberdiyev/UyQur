from django.urls import path, include 

from core.apps.accounts.views.login import LoginApiView, TestApiView

urlpatterns = [
    path('auth/login/', LoginApiView.as_view(), name='login'),
    path('test/', TestApiView.as_view()),
]