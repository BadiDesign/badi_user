import datetime
import random
import string
from datetime import timedelta

from badi_blog.api.api import CustomPagination
from badi_user.api.api import UserViewSet, MemberViewSet
from badi_utils.email import Email
from badi_utils.errors import BadiErrorCodes
from badi_utils.validations import PersianValidations, BadiValidators
from django.contrib.auth import login, validators
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.http import JsonResponse, Http404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from badi_utils.dynamic_api import DynamicModelApi, InCaseSensitiveTokenObtainPairSerializer, CustomValidation
from badi_utils.logging import log
from badi_utils.responses import ResponseOk, ResponseNotOk
from badi_utils.utils import random_with_N_digits, permissions_json
from rest_framework_simplejwt.views import TokenRefreshView
from badi_user.api.serializers import UserSerializer, GroupSerializer, MemberSerializer, LogSerializer
from badi_user.filter import UserListFilter, MemberListFilter, LogFilter
from django.utils.translation import gettext_lazy as _
from badi_utils.sms import IpPanelSms
from django.conf import settings

from account.api.serializers import CustomMemberSerializer
from account.filter import CustomMemberFilter
from account.models import User


class CustomUserViewSet(UserViewSet):
    columns = ['id', 'picture', 'username', 'first_name', 'last_name', 'mobile_number', 'is_admin', 'is_active',
               'email', ]
    order_columns = ['id', 'picture', 'username', 'first_name', 'last_name', 'mobile_number', 'is_admin', 'is_active',
                     'email', ]
    model = User
    queryset = User.objects.filter(is_admin=True)
    serializer_class = UserSerializer
    custom_perms = {
        'self': True
    }
    switches = {
        'is_active': {
            'true': ' ',
            'false': ' ',
        }
    }

    @action(methods=['put'], detail=False, url_path='change_state/(?P<pk>[^/.]+)')
    def change_state(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        user.is_active = not user.is_active
        user.save()

        return JsonResponse({
            'message': 'با موفقیت {0} شد'.format('فعال' if user.is_active else 'غیرفعال')
        })


class CustomMemberViewSet(MemberViewSet):
    columns = ['id', 'id', 'picture', 'username', 'first_name', 'last_name', 'amount', 'title', 'level', 'level_expired']
    order_columns = ['id', 'id', 'picture', 'username', 'first_name', 'last_name', 'amount', 'title', 'level',
                     'level_expired']
    model = User
    queryset = User.objects.filter(is_admin=False)
    serializer_class = CustomMemberSerializer
    custom_perms = {
        'self': True,
        'update_self': True,
    }

    def filter_queryset(self, qs):
        if self.action == 'datatable':
            return CustomMemberFilter(self.request.POST).qs.filter(is_admin=False)
        return super().filter_queryset(qs)

    def render_column(self, row, column):
        if column == 'transactions__count':
            return row.transactions.count()
        return super().render_column(row, column)

    @action(methods=['get'], detail=False)
    def chart(self, request, *args, **kwargs):
        today = datetime.datetime.today()
        start_of_month = datetime.datetime.today()
        members = User.objects.filter(is_admin=False)
        MONTH_NAMES = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن",
                       "اسفند"]
        data = {
            "data-new-members-today": members.filter(date_joined=today).count(),
            "data-new-members-week": members.filter(date_joined__gte=today - datetime.timedelta(days=7)).count(),
            "data-all-personnels-count": User.objects.filter(is_admin=True).count(),
            "data-all-members-count": members.count(),
            "data": [{
                'name': 'کاربران جدید',
                'data': [members.filter(
                    date_joined__month=(start_of_month - datetime.timedelta(days=30 * x)).month,
                    date_joined__year=(start_of_month - datetime.timedelta(days=30 * x)).year
                ).count() for x in range(7)]
            }],
            'labels': [MONTH_NAMES[(start_of_month - datetime.timedelta(days=30 * x)).month - 1] for x in range(7)]
        }
        return Response(data)
