import random
import re
import string
from random import randint
from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .dynamic_api import CustomValidation


class CustomAccessMixin(AccessMixin):
    permission_required = None

    def handle_no_permission(self):
        messages.error(self.request, _('NO_PERMISSION'))
        return redirect('/')


class CustomPermissionRequiredMixin(CustomAccessMixin):
    """Verify that the current user has all specified permissions."""
    permission_required = None

    def get_permission_required(self):
        return self.permission_required

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        if self.permission_required is False:
            return True
        else:
            return self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


def clean_cost(cost: str):
    cost = cost.split(' ')
    cost = cost[0].split(',')
    cost = ''.join(cost)
    return cost


def permissions_json():
    apps1 = assignable_app_names()
    permission = dict()
    for app in apps1:

        data_to_return = []
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            perms = Permission.objects.filter(~Q(name__icontains='can'), content_type__app_label=app.app_label)
        else:
            perms = Permission.objects.filter(~Q(name__icontains='can'), content_type__app_label=app['app_label'])

        for perm in perms:
            data_to_return.append({
                'id': perm.id,
                'name': perm.name,
                'content_type': perm.content_type.app_label,
                'codename': perm.codename,
            })
        if len(data_to_return) != 0:
            if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
                permission[apps.get_app_config(app.app_label).verbose_name] = data_to_return
            else:
                permission[apps.get_app_config(app['app_label']).verbose_name] = data_to_return

    return permission


def assignable_app_names():
    if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
        apps1 = ContentType.objects.filter().distinct('app_label')
    else:
        apps1 = ContentType.objects.filter().values('app_label').distinct()
    return apps1


def is_valid_iran_code(input):
    if not re.search(r'^\d{10}$', input):
        return False

    check = int(input[9])
    s = sum([int(input[x]) * (10 - x) for x in range(9)]) % 11
    return (s < 2 and check == s) or (s >= 2 and check + s == 11)


class PermissionsApi(APIView):
    user_permission = None

    def check_permissions(self, request):
        """
         برای دادن پرمیشن ها به هر کاربر برای حق دسترسی به قسمت های مختلف
        """
        if not self.request.user.is_authenticated:
            self.permission_denied(
                request, message=getattr('Login Required', 'message', None)
            )
        if self.user_permission:
            exists = self.request.user.user_permissions.filter(
                codename=self.user_permission.split('.')[1]).exists()
            if not self.request.user.is_superuser and not exists:
                self.permission_denied(
                    request, message=getattr(self.user_permission, 'message', None)
                )


def getToken(user):
    return RefreshToken.for_user(user)


def checkEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def has_numbers(string):
    #  hasNumbers("I own 1 dog") => True
    #  hasNumbers("I own no dog") => False
    return any(char.isdigit() for char in string)


def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def set_many2many(initial_data, field, instance, model_many, key=None, many_key='title'):
    if key is None:
        key = field
    res = initial_data.getlist(field)
    allmany_object = []
    for val in res:
        many_object, was_created = model_many.objects.get_or_create(**{many_key + '': val})
        allmany_object.append(many_object.pk)
    instance.__getattribute__(key).set(allmany_object)
    instance.save()


def check_many2many(initial_data, field, error='', empty=False):
    res = initial_data.getlist(field)
    if res and type([]) == type(res):
        return res
    else:
        if not empty:
            raise CustomValidation(field, error)
        return 0


def file_size(value):  # add this to some file where you can import it from
    limit = 1 * 1024 * 1024
    err = None
    try:
        if value and value.size > limit:
            err = True
            raise ValidationError('حجم فایل باید کمتر از 1 مگابایت باشد!')
    except:
        if err:
            raise ValidationError('حجم فایل باید کمتر از 1 مگابایت باشد!')
        print(value.url + ' NOT FOUND!!!')


def video_file(value):  # add this to some file where you can import it from
    limit = 500 * 1024 * 1024
    try:
        if value and value.size > limit:
            raise ValidationError('حجم فایل باید کمتر از 500 مگابایت باشد!')
    except:
        print(value.url + ' NOT FOUND!!!')
