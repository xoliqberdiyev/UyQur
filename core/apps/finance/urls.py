from django.urls import path, include

from core.apps.finance.views import cash_transaction as cash_views
from core.apps.finance.views import cash_transaction_folder as folder_views
from core.apps.finance.views import payment_type as pt_views
from core.apps.finance.views import type_income as ti_views
from core.apps.finance.views import income as income_views
from core.apps.finance.views import expence_type as ex_views
from core.apps.finance.views import expence as expence_views


urlpatterns = [
    path('cash_transaction/', include(
        [
            path('list/', cash_views.CashTransactionListApiView.as_view()),
            path('create/', cash_views.CashTransactionCreateApiView.as_view()),
            path('<uuid:id>/delete/', cash_views.CashTransactionDeleteApiView.as_view()),
            path('<uuid:id>/update/', cash_views.CashTransactionUpdateApiView.as_view()),
            path('statistics/', cash_views.CashTransactionStatisticsApiView.as_view()),
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
    )),
    path('type_income/', include(
        [
            path('create/', ti_views.TypeIncomeCreateApiView.as_view()),
            path('list/', ti_views.TypeIncomeListApiView.as_view()),
            path('<uuid:id>/update/', ti_views.TypeIncomeUpdateApiView.as_view()),
            path('<uuid:id>/delete/', ti_views.TypeIncomeDeleteApiView.as_view()),
        ]
    )),
    path('income/', include(
        [
            path('list/', income_views.IncomeListApiView.as_view()),
            path('create/', income_views.IncomeCreateApiView.as_view()),
            path('<uuid:counterparty_id>/list/', income_views.CounterpartyIncomeListApiView.as_view()),
        ]
    )),
    path('expence_type/', include(
        [
            path('list/', ex_views.ExpenceTypeListApiView.as_view()),
            path('create/', ex_views.ExpenceTypeCreateApiView.as_view()),
            path('<uuid:id>/update/', ex_views.ExpenceTypeUpdateApiView.as_view()),
            path('<uuid:id>/delete/', ex_views.ExpenceTypeDeleteApiView.as_view()),
        ]
    )),
    path('expence/', include(
        [
            path('list/', expence_views.ExpenceListApiView.as_view()),
            path('create/', expence_views.ExpenceCreateApiView.as_view()),
            path('<uuid:counterparty_id>/list/', expence_views.CounterpartyExpenceListApiView.as_view()),
        ]
    ))
]