import datetime

from badi_utils.dynamic_models import BadiModel
from django.conf import settings
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models

from badi_utils.utils import random_with_N_digits
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()
BANK_TRANSACTION_MODEL = getattr(settings, "BANK_TRANSACTION_MODEL", "badi_wallet.BankTransaction")


class DiscountCode(models.Model, BadiModel):
    class Meta:
        verbose_name = _("DiscountCode")
        verbose_name_plural = _("DiscountCodes")
        permissions = (
            ('can_discount_code', _("Manage") + ' ' + verbose_name_plural),
        )

    CODE_TYPES = (
        ('$', _("Money")),
        ('%', _("Percent")),
    )

    type = models.CharField(max_length=10, choices=CODE_TYPES, verbose_name=_("Type"))
    code = models.CharField(max_length=10, unique=True, verbose_name=_("Code"))
    amount = models.BigIntegerField(default=0, verbose_name=_("Amount"), validators=[MinValueValidator(0)])
    percent = models.IntegerField(default=0, verbose_name=_("Percent"),
                                  validators=[MaxValueValidator(101), MinValueValidator(-1)])
    use_count = models.IntegerField(default=0, verbose_name=_("Use count"))
    use_max = models.IntegerField(default=1, verbose_name=_("Use max"))
    expire_date = models.DateField(verbose_name=_("Expire Date"))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Created at"))

    def use(self):
        self.use_count += 1
        self.save()

    def is_usable(self):
        if self.use_count > self.use_max:
            return False
        if datetime.date.today() > self.expire_date:
            return False
        return True

    def calc(self, amount):
        if self.type == '$':
            return amount - self.amount
        else:
            return amount - (amount * self.percent / 100)


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
    info = models.TextField(verbose_name=_("Info"), blank=True)
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
        ('1', _("Buy")),
        ('+', _("Charge")),
        ('m', _("Charge by Management")),
        ('-', _("Refund")),
    )

    user = models.ForeignKey(User, related_name='transactions', on_delete=models.PROTECT, verbose_name=_("User"))
    amount = models.BigIntegerField(default=0, verbose_name=_("Amount"))
    type = models.CharField(max_length=2, choices=TYPES, verbose_name=_("Type"))
    info = models.TextField(blank=True, verbose_name=_("Info"))
    date_time = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Time"))
    subject = models.CharField(max_length=255, verbose_name=_("Transaction Subject"), null=True, blank=True)
    bank_transaction = models.ForeignKey(BANK_TRANSACTION_MODEL, related_name='transactions', null=True, blank=True,
                                         on_delete=models.PROTECT, verbose_name=_("Bank Transaction"))
    discount_code = models.ForeignKey(DiscountCode, related_name='transactions', null=True, blank=True,
                                      verbose_name=_("DiscountCode"), on_delete=models.PROTECT)

    @staticmethod
    def for_user(user):
        return Transaction.objects.filter(user=user)
