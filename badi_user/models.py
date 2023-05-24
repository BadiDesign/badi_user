from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django_resized import ResizedImageField

from badi_utils.dynamic_models import BadiModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    token = models.CharField(max_length=250, verbose_name=_('code'))
    is_forgot = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    last_send = models.DateTimeField(blank=True, null=True)

    def is_enabled(self):
        return self.created_at > datetime.now() - timedelta(minutes=30)

    def is_active(self):
        return self.last_send > datetime.now() - timedelta(minutes=30)

    def is_possible_resend(self):
        if self.last_send:
            return self.last_send > datetime.now() - timedelta(minutes=5)
        return True


class BadiAbstractUser(AbstractUser):
    class Meta:
        verbose_name = _('User')
        abstract = True
        verbose_name_plural = _('Users')
        permissions = (
            ('can_user', _("Manage") + ' ' + _(verbose_name)),
            ('can_member', _("Manage") + ' ' + _("Member")),
        )

    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))
    mobile_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('Mobile Number'))
    birth_date = models.DateField(verbose_name=_('Birth Date'), null=True)
    picture = ResizedImageField(quality=99, size=[450, 450], blank=True, null=True, upload_to='public/user/',
                                force_format="WEBP")
    token = models.ForeignKey(Token, null=True, blank=True, verbose_name=_('Token'), related_name='user',
                              on_delete=models.SET_NULL)
    amount = models.BigIntegerField(default=0, blank=True, verbose_name=_('Amount'))
    last_action = models.DateTimeField(blank=True, null=True, verbose_name='Last Action')

    def __str__(self):
        return self.first_name + " " + self.last_name

    def update_action(self):
        self.last_action = datetime.now()
        self.save()

    @staticmethod
    def admins():
        return User.objects.filter(is_admin=True)

    @staticmethod
    def members():
        return User.objects.filter(is_admin=False)

    def is_administrator(self):
        return self.is_admin

    def is_member(self):
        return not self.is_admin

    def get_full_name(self):
        return super().get_full_name() if self.first_name else self.username

    @classmethod
    def get_form_fields(cls, action, *args):
        if action == 'member_create':
            return ['username', 'password', 'first_name', 'picture', 'last_name', 'is_admin', 'mobile_number']
        if action == 'member_update':
            return ['username', 'password', 'first_name', 'picture', 'last_name', 'is_admin', 'mobile_number']
        if action == 'member_self_update':
            return ['username', 'password', 'first_name', 'picture', 'last_name', 'mobile_number']
        if action == 'user_create':
            return ['username', 'password', 'first_name', 'picture', 'last_name', 'is_admin', 'mobile_number', 'email']
        if action == 'UserSerializer':
            return ['id', 'username', 'password', 'picture', 'first_name', 'last_name', 'mobile_number', 'is_admin',
                    'mobile_number', ]
        return ['first_name', 'last_name', 'mobile_number', 'picture']

    @classmethod
    def get_datatable_cols(cls, class_name, *args):
        if class_name == 'MemberListView':
            return ['#', _("Select"), "", _("Username"), _("FirstName"), _("LastName"), _("Amount")]
        return [_("FirstName"), _("LastName"), _("Mobile Number"), _("Picture")]

    @staticmethod
    def get_api_url(view):
        if view == 'MemberListView':
            return '/api/v1/member/'

    def success_transaction(self, trans, request):
        # transAction = Transaction(
        #     user=trans.user,
        #     amount=trans.amount,
        #     type='1',
        #     subject='شارژ حساب کاربری',
        #     bank_transaction=trans,
        # )
        # transAction.save()
        # trans.user.amount += trans.amount
        print("SUCCESS_TRANSACTION", self, trans, request)


class User(BadiAbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Notification(models.Model):
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        permissions = (
            ('can_notification', _("Manage") + ' ' + _(verbose_name)),
        )

    user = models.ForeignKey(get_user_model(), related_name='notifications', on_delete=models.CASCADE,
                             verbose_name=_('User'))
    subject = models.CharField(max_length=255, verbose_name=_('Subject'))
    text = models.TextField(verbose_name=_('Text'))
    show_date = models.DateField(verbose_name=_('Show Date'))
    is_seen = models.BooleanField(default=False, verbose_name=_('Is Seen'))

    def __str__(self):
        return "{0} - {1}".format(self.subject, self.user)


class Log(models.Model):
    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')
        permissions = (
            ('can_log', _("Manage") + ' ' + _(verbose_name)),
        )
        ordering = ['-pk']

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    user = models.ForeignKey(get_user_model(), related_name='logs', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name=_('User'))
    priority = models.IntegerField(verbose_name=_('Priority'))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    description = models.TextField(verbose_name=_('Description'), validators=[MaxLengthValidator(1200)])
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.title

    @staticmethod
    def get_serializer_fields():
        return ['title', 'user', 'priority', 'status', 'description', 'created_at', ]

    @staticmethod
    def get_datatable_columns():
        return ["#", _('Title'), _('User'), _('Priority'), _('Status'), _('Description'), _('Created at')]
