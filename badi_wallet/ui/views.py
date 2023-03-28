from django.views import View
from django.utils.translation import gettext_lazy as _
from badi_utils.dynamic import DynamicListView
from badi_wallet.action import MERCHANT, ZP_API_VERIFY, ZPBankAction
from badi_wallet.models import Transaction, BankTransaction


class TransActionsView(DynamicListView):
    model = Transaction
    datatable_cols = ['#', 'مبلغ', 'نوع', 'زمان ثبت', 'موضوع', 'توضیحات']


class AdminTransActionsView(DynamicListView):
    model = Transaction
    datatable_cols = Transaction().get_datatable_verbose_names(['bank transaction'])
    datatableURL = '/api/v1/transaction/all_transactions/'
    template_name = 'transaction/all_transaction_list.html'


class ZPVerifyTransActionsView(View):
    bankError = _("The operation encountered an error. Please try again."
                  " If the amount is deducted from your account, it will be returned to your account within 72 hours.")

    def get(self, request, *args, **kwargs):
        t_status = request.GET.get('Status')
        t_authority = request.GET.get('Authority')
        return ZPBankAction().get_bank_response(request, t_status, t_authority)
