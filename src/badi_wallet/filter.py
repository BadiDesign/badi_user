from django_filters import rest_framework as filters
from badi_user.filter import TextIn
from badi_wallet.action import Transaction


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = [
            'user'
        ]

    # date_time = filters.DateFromToRangeFilter(label='تاریخ')
    # amount = filters.NumericRangeFilter(label='مبلغ')
    subject = TextIn(field_name='subject')
