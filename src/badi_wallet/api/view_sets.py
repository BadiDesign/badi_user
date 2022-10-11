import json
from django.db.models import Q
from django.http import Http404
from django_datatables_view.mixins import LazyEncoder
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from badi_utils.dynamic_api import CustomValidation, DynamicModelReadOnlyApi
from badi_wallet.action import ZPBankAction
from badi_utils.responses import ResponseOk
from badi_utils.date_calc import custom_change_date
from badi_wallet.api.serializers import TransactionSerializer
from badi_wallet.models import Transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class TransactionViewSet(DynamicModelReadOnlyApi):
    permission_classes = [permissions.IsAuthenticated]
    columns = ['id', 'amount', 'type', 'date_time', 'subject']
    order_columns = ['id', 'amount', 'type', 'date_time', 'subject']
    model = Transaction
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    disables_views = [
        'update', 'create', 'list', 'retrieve', 'destroy', 'delete'
    ]
    custom_perms = {
    }

    @action(methods=['post'], detail=False)
    def charge_request(self, request, *args, **kwargs):
        res = ZPBankAction().send_request(request=request, amount=self.request.data.get('amount'),
                                          mobile=self.request.data.get('mobile_number'),
                                          email=self.request.data.get('email'))
        return res

    @action(methods=['get'], detail=False)
    def verify(self, request, *args, **kwargs):
        res = ZPBankAction().verify(request=request)
        return res

    @action(methods=['put'], detail=False, url_path='increase_wallet/(?P<pk>[^/.]+)')
    def increase_wallet(self, request, pk, *args, **kwargs):
        if not self.request.user.is_admin and not self.request.user.is_admin:
            raise Http404
        user = get_object_or_404(User, pk=pk, is_admin=False)
        try:
            amount = int(self.request.data.get('amount'))
        except:
            raise CustomValidation('amount', "مبلغ وارد شده صحیح نمی باشد")
        user.amount += amount
        user.save()
        get = self.request.data.get('description', 'بدون توضیحات')
        Transaction(user=user, amount=amount, type='1',
                    subject='برداشت توسط ' + self.request.user.get_full_name() + ' : ' + get).save()
        return ResponseOk()

    @action(methods=['put'], detail=False, url_path='decease_wallet/(?P<pk>[^/.]+)')
    def decease_wallet(self, request, pk, *args, **kwargs):
        if not self.request.user.is_admin and not self.request.user.is_admin:
            raise Http404
        user = get_object_or_404(User, pk=pk, is_admin=False)
        try:
            amount = int(self.request.data.get('amount'))
        except:
            raise CustomValidation('amount', "مبلغ وارد شده صحیح نمی باشد")
        if amount < 1:
            raise CustomValidation('amount', "مبلغ وارد شده کمتر از 1 می باشد")
        if user.amount < amount:
            raise CustomValidation('amount', "مبلغ وارد شده بیشتر از موجودی کیف پول کاربر می باشد")
        user.amount -= amount
        user.save()
        get = self.request.data.get('description', 'بدون توضیحات')
        Transaction(user=user, amount=amount, type='6',
                    subject='شارژ توسط ' + self.request.user.get_full_name() + ' : ' + get).save()
        return ResponseOk()

    @action(methods=['post'], detail=False)
    def all_transactions(self, request, *args, **kwargs):
        if 'datatable' in self.disables_views:
            return Http404()
        response = None
        func_val = self.get_context_data(**kwargs)
        if not self.is_clean:
            assert isinstance(func_val, dict)
            response = dict(func_val)
            if 'error' not in response and 'sError' not in response:
                response['result'] = 'ok'
            else:
                response['result'] = 'error'
        else:
            response = func_val

        dump = json.dumps(response, cls=LazyEncoder)
        return self.render_to_response(dump)

    def get_columns(self):
        if self.action == 'all_transactions':
            return ['id', 'user', 'amount', 'type', 'date_time', 'subject']
        return super(TransactionViewSet, self).get_columns()

    def render_column(self, row, column):
        if column == 'user':
            if row.user.first_name and row.user.last_name:
                return row.user.first_name + " " + row.user.last_name
            return row.username

        return super(TransactionViewSet, self).render_column(row, column)

    def filter_queryset(self, qs):
        if self.action == 'all_transactions':
            qs = Transaction.objects.all()
        else:
            qs = Transaction.for_user(self.request.user)
        search = self.request.POST.get('search[value]', None)
        if search:
            qs = qs.filter(Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search))
        return qs

    def ordering(self, qs):
        return super().ordering(qs.order_by('-pk'))
