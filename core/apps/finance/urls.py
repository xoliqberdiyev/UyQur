from django.urls import path, include

from core.apps.finance.views import cash_transaction as cash_views
from core.apps.finance.views import cash_transaction_folder as folder_views
from core.apps.finance.views import payment_type as pt_views


urlpatterns = [
    path('cash_transaction/', include(
        [
            path('list/', cash_views.CashTransactionListApiView.as_view()),
            path('create/', cash_views.CashTransactionCreateApiView.as_view()),
            path('<uuid:id>/delete/', cash_views.CashTransactionDeleteApiView.as_view()),
            path('<uuid:id>/update/', cash_views.CashTransactionUpdateApiView.as_view()),
        ]
    )),
    path('cash_transaction_folder/', include(
        [
            path('create/', folder_views.CashTransactionCreateApiView.as_view()),
            path('list/', folder_views.CashTransactionFolderListApiView.as_view()),
            path('<uuid:id>/delete/', folder_views.CashTransactionFolderDeleteApiView.as_view()),
            path('<uuid:id>/update/', folder_views.CashTransactionFolderUpdateApiView.as_view()),
        ]
    )),
    path('payment_type/', include(
        [
            path('create/', pt_views.PaymentTypeCreateApiView.as_view()),
            path('list/', pt_views.PaymentListApiView.as_view()),
            path('<uuid:id>/delete/', pt_views.PaymentDeleteApiView.as_view()),
            path('<uuid:id>/update/', pt_views.PaymentUpdateApiView.as_view()),
        ]
    ))
]