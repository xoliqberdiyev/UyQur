from django.urls import path, include

from core.apps.products.views import product as product_views
from core.apps.products.views import unity as unity_views
from core.apps.products.views import folder as folder_views


urlpatterns = [
    path('product/', include(
        [
            path('list/', product_views.ProductListApiView.as_view()),
            path('create/', product_views.ProductCreateApiView.as_view()),
            path('<uuid:product_id>/update/', product_views.ProductUpdateApiView.as_view()),
            path('<uuid:product_id>/delete/', product_views.ProductDeleteApiView.as_view()),
        ]
    )),
    path('unity/', include(
        [
            path('list/', unity_views.UnityListApiView.as_view()),
        ]
    )),
    path('folder/', include(
        [
            path('create/', folder_views.FolderCreateApiView.as_view()),
            path('list/', folder_views.FolderListApiView.as_view()),
            path('<uuid:id>/update/', folder_views.FolderUdateApiView.as_view()),
            path('<uuid:id>/delete/', folder_views.FolderDeleteApiView.as_view()),
            path('sub_folder/', include(
                [
                    path('create/', folder_views.SubFolderCreateApiView.as_view()),
                    path('<uuid:folder_id>/list/', folder_views.SubFolderListByFolderIdApiView.as_view()),
                    path('<uuid:id>/delete/', folder_views.SubFolderDeleteApiView.as_view()),
                    path('<uuid:id>/update/', folder_views.SubFolderUpdateApiView.as_view()),
                ]
            )),
        ]
    )),
]