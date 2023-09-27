from django.views import View
from django.utils.translation import gettext_lazy as _
from badi_utils.dynamic import DynamicListView, DynamicCreateView, DynamicUpdateView
from badi_wallet.action import MERCHANT, ZP_API_VERIFY, ZPBankAction
from badi_wallet.filter import TransactionFilter
from badi_wallet.models import Transaction, BankTransaction, DiscountCode


class TransActionsView(DynamicListView):
    model = Transaction
    datatable_cols = ['#', 'مبلغ', 'نوع', 'زمان ثبت', 'موضوع', 'توضیحات']


class AdminTransActionsView(DynamicListView):
    model = Transaction
    datatable_cols = Transaction().get_datatable_verbose_names([_("Bank Transaction"), _("DiscountCode"), ])
    datatableURL = '/api/v1/transaction/all_transactions/'
    template_name = 'transaction/all_transaction_list.html'
    extra_context = {
        'filter_form': TransactionFilter().form
    }


class ReportTransActionsView(DynamicListView):
    model = Transaction
    template_name = 'transaction/all_transaction_report.html'
    extra_context = {
        'form': TransactionFilter().form
    }


class ZPVerifyTransActionsView(View):
    bankError = _("The operation encountered an error. Please try again."
                  " If the amount is deducted from your account, it will be returned to your account within 72 hours.")

    def get(self, request, *args, **kwargs):
        t_status = request.GET.get('Status')
        t_authority = request.GET.get('Authority')
        return ZPBankAction().get_bank_response(request, t_status, t_authority)


class DiscountCodeCreateView(DynamicCreateView):
    model = DiscountCode
    datatable_cols = model().get_datatable_verbose_names()


class DiscountCodeUpdateView(DynamicUpdateView):
    model = DiscountCode
