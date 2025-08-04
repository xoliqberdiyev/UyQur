from django.urls import path, include

from core.apps.finance.views import cash_transaction as cash_views


urlpatterns = [
    path('cash_transaction/', include(
        [
            path('list/', cash_views.CashTransactionListApiView.as_view()),
        ]
    ))
]