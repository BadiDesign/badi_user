from django.views.decorators.csrf import csrf_exempt

from badi_utils.dynamic import *
from .views import *

urlpatterns = [
    path('transactions', TransActionsView.as_view(), name='transactions'),
    path('all_transactions', AdminTransActionsView.as_view(), name='all_transactions'),
    path('all_transactions_report', ReportTransActionsView.as_view(), name='all_transactions_report'),
    path('zp_verify', ZPVerifyTransActionsView.as_view(), name='zp_verify'),
    # path('idp_verify', csrf_exempt(IDPVerifyTransActionsView.as_view()), name='idp_verify'),
]
