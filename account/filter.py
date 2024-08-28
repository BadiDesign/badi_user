from badi_user.filter import MemberListFilter, UserListFilter, TextIn
from django.db.models import Q

from account.models import User
from django_filters import rest_framework as filters


class CustomUserFilter(UserListFilter):
    class Meta:
        model = User
        fields = [
        ]


class CustomMemberFilter(MemberListFilter):
    class Meta:
        model = User
        fields = [
        ]
