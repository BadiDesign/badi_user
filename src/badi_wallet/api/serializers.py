from badi_utils.dynamic_api import api_error_creator, DynamicSerializer
from badi_wallet.models import Transaction


class TransactionSerializer(DynamicSerializer):
    class Meta:
        model = Transaction
        extra_kwargs = api_error_creator(Transaction, ['amount', 'type', 'date_time', 'subject'],
                                         blank_fields=[],
                                         required_fields=['amount', 'type', 'date_time', 'subject'])
        fields = ['id', 'amount', 'type', 'date_time', 'subject']
