from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Token(models.Model):
    token = models.CharField(max_length=250, verbose_name=_('کد'))
    is_forgot = models.BooleanField(default=False, verbose_name=_('فراموشی رمز عبور'))
    is_accepted = models.BooleanField(default=False, verbose_name=_('تایید شده'))
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('شماره تماس'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("زمان"))
    last_send = models.DateTimeField(blank=True, null=True, verbose_name=_("آخرین ارسال"))

    def is_enabled(self):
        return self.created_at > datetime.now() - timedelta(minutes=30)

    def is_active(self):
        return self.last_send > datetime.now() - timedelta(minutes=30)

    def is_possible_resend(self):
        if self.last_send:
            return self.last_send > datetime.now() - timedelta(minutes=5)
        return True


class User(AbstractUser):
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
        permissions = (
            ('can_user', _('مدیریت کاربران')),
        )

    is_admin = models.BooleanField(default=False, verbose_name=_('کاربر مدیر'))
    mobile_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('شماره موبایل'))
    birth_date = models.DateField(verbose_name=_('تاریخ تولد'), null=True)
    picture = models.ImageField(null=True, verbose_name=_('تصویر'), upload_to='public/user', blank=True)
    token = models.ForeignKey(Token, null=True, blank=True, verbose_name=_('توکن'), related_name='user',
                              on_delete=models.SET_NULL)
    amount = models.BigIntegerField(default=0, blank=True, verbose_name=_('موجودی کیف پول'))

    def __str__(self):
        return self.first_name + " " + self.last_name

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


class Notification(models.Model):
    class Meta:
        verbose_name = _('اعلان')
        verbose_name_plural = _('اعلان ها')
        permissions = (
            ('can_notification', _('مدیرت اعلان ها')),
        )

    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE, verbose_name=_('کاربر'))
    subject = models.CharField(max_length=255, verbose_name=_('موضوع'))
    text = models.TextField(verbose_name=_('متن'))
    show_date = models.DateField(verbose_name=_('نمایش اعلان از تاریخ'))
    is_seen = models.BooleanField(default=False, verbose_name=_('خوانده شده'))

    def __str__(self):
        return "{0} - {1}".format(self.subject, self.user)


class Log(models.Model):
    class Meta:
        verbose_name = _('گزارشات سامانه')
        verbose_name_plural = _('گزارشات سامانه')
        permissions = (
            ('can_log', _('مشاهده گزارشات سامانه')),
        )

    title = models.CharField(max_length=200, verbose_name=_('عنوان'))
    user = models.ForeignKey(User, related_name='logs', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name=_('کاربر'))
    priority = models.IntegerField(verbose_name=_('اهمیت'))
    status = models.BooleanField(default=True, verbose_name=_('وضیعت'))
    description = models.TextField(verbose_name=_('توضیحات'), validators=[MaxLengthValidator(1200)])
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_('زمان'))

    def __str__(self):
        return self.title
