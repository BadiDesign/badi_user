from badi_utils.dynamic_models import BadiModel
from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models

from badi_utils.utils import random_with_N_digits
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()
BANK_TRANSACTION_MODEL = getattr(settings, "BANK_TRANSACTION_MODEL", "badi_wallet.BankTransaction")


class BankTransaction(models.Model, BadiModel):
    class Meta:
        verbose_name = _("Bank Transaction")
        verbose_name_plural = _("Bank Transaction")
        permissions = (
            ('can_bank_transaction', _("Manage") + " " + verbose_name_plural),
        )

    authority = models.CharField(max_length=255, unique=True, verbose_name=_("Authority"))
    user = models.ForeignKey(User, related_name='bank_transactions', on_delete=models.PROTECT, verbose_name=_("User"))
    description = models.TextField(verbose_name=_("Description"), blank=True, validators=[MaxLengthValidator(1200)])
    is_verified = models.BooleanField(default=False, verbose_name=_("is Verified"))
    ref_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("RefID"))
    card_hash = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Card Hash"))
    order_id = models.CharField(max_length=50, blank=True, null=True)
    amount = models.BigIntegerField(default=0, verbose_name=_("Amount"))
    data = models.TextField(verbose_name=_("Bank Response"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    @staticmethod
    def generate_unique_order_id():
        while True:
            created = random_with_N_digits(49)
            if not BankTransaction.objects.filter(order_id=created).exists():
                return created


class Transaction(models.Model, BadiModel):
    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        permissions = (
            ('can_transaction', _("Manage") + ' ' + verbose_name_plural),
        )

    TYPES = (
        ('+', _("Charge")),
        ('-', _("Return")),
    )

    user = models.ForeignKey(User, related_name='transactions', on_delete=models.PROTECT, verbose_name=_("User"))
    amount = models.BigIntegerField(default=0, verbose_name=_("Amount"))
    type = models.CharField(max_length=2, choices=TYPES, verbose_name=_("Type"))
    date_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Time"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"), null=True, blank=True)
    bank_transaction = models.ForeignKey(BANK_TRANSACTION_MODEL, related_name='transactions', null=True, blank=True,
                                         on_delete=models.PROTECT)

    @staticmethod
    def for_user(user):
        return Transaction.objects.filter(user=user)
