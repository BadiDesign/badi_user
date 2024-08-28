from datetime import timedelta, datetime, date
from badi_user.models import User as BadiUser
from badi_utils.dynamic_models import BadiModel
from badi_utils.sms import IpPanelSms
from badi_utils.validations import PersianValidations
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.apps import apps as django_apps


def file_size(value):
    limit = 0.5 * 1024 * 1024
    err = None
    try:
        if value and value.size > limit:
            err = True
            raise ValidationError('حجم فایل باید کمتر از 1 مگابایت باشد!')
    except:
        if err:
            raise ValidationError('حجم فایل باید کمتر از 1 مگابایت باشد!')
        print(value.url + ' NOT FOUND!!!')


class User(BadiUser):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        permissions = (
            ('can_user', _('Manage users')),
            ('can_member', _('Manage members')),
        )

    USER_LEVELS = (
        ('normal', 'معمولی'),
        ('premium', 'پرمیوم'),
    )

    national_code = models.CharField(max_length=10, null=True, verbose_name="کد ملی")
    picture = models.ImageField(null=True, verbose_name='تصویر', upload_to='company/ads', blank=True,
                                validators=[file_size])
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name="عنوان تجاری")
    call_number = models.CharField(max_length=250, null=True, blank=True, verbose_name='شماره ثابت')
    address = models.TextField(blank=True, verbose_name='آدرس')
    plaque = models.CharField(max_length=20, null=True, blank=True, verbose_name="پلاک")
    level = models.CharField(max_length=8, choices=USER_LEVELS, verbose_name='سطح کاربری', default='normal')
    level_expired = models.DateField(blank=True, null=True, verbose_name="انقضا سطح کاربری")

    def update_action(self):
        if self.level_expired and self.level_expired < date.today() and self.level != 'normal':
            self.level = 'normal'
            self.save()
        super().update_action()

    def get_remaining_days(self):
        if self.level_expired:
            return (self.level_expired - date.today()).days
        return 0

    @classmethod
    def get_form_fields(cls, action, *args):
        if action == 'profile':
            return ['id', 'first_name', 'last_name', 'picture']
        if action in ['member_create', 'member_update']:
            return ['picture', 'username', 'password', 'first_name', 'last_name', 'is_admin', 'mobile_number', 'level',
                    'level_expired', 'plaque',  'title', 'call_number', 'national_code', 'address', ]
        if action in ['user_create', 'user_update']:
            return ['picture', 'username', 'password', 'first_name', 'last_name', 'is_admin', 'mobile_number', ]
        if action in ['member_self_update']:
            return ['first_name', 'last_name', 'title', 'address', 'picture',  'plaque', 'call_number', ]
        if action in ['UserSerializer']:
            return ['username', 'password', 'picture', 'first_name', 'last_name', 'mobile_number', 'is_admin',
                    'mobile_number', ]
        return ['first_name', 'last_name', 'mobile_number', 'picture', ]

    @classmethod
    def get_datatable_cols(cls, class_name, *args):
        if class_name == 'MemberListView':
            return ['#', _("Select"), _("Picture"), _("Username"), _("FirstName"), _("LastName"), 'موجودی',
                    'عنوان ',  'سطح کاربری', 'انقضا سطح کاربری', ]
        if class_name == 'UserListView':
            return ['#', _("Picture"), 'شماره تماس', "مدیر", 'فعال']
        return ['نام', 'نام خانوادگی', 'شماره تماس', 'تصویر']

    def has_level(self, level):
        if self.level == 'normal' and level in ['normal']:
            return True
        if self.level == 'premium' and level in ['premium', 'normal']:
            return True
        return False

    def __str__(self):
        if len(super().__str__().split(' ')[0]):
            return super().__str__()
        return self.username

    def is_premium(self):
        return self.level == 'premium'
