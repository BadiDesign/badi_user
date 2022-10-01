from django.db.models import Value, Q
from django.db.models.functions import Concat
from django_filters import rest_framework as filters
from badi_utils.date_calc import custom_change_date
from django.contrib.auth import get_user_model

User = get_user_model()


class BadiFilterBase:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'field_name' not in kwargs:
            raise Exception("Enter field_name in filter field")
        self.field_name = kwargs['field_name']


class BadiDateSmallerFilter(BadiFilterBase, filters.CharFilter):

    def filter(self, qs, value):
        if len(value) > 10:
            value = custom_change_date(value, 3)
            return qs.filter(**{self.field_name + '__lt': value})
        else:
            return qs


class BadiDateLargerFilter(BadiFilterBase, filters.CharFilter):

    def filter(self, qs, value):
        if len(value) > 15:
            value = custom_change_date(value, 3)
            return qs.filter(**{self.field_name + '__gt': value})
        else:
            return qs


class TextIn(BadiFilterBase, filters.CharFilter):

    def filter(self, qs, value):
        if len(value) > 0:
            return qs.filter(**{self.field_name + '__icontains': value})
        else:
            return qs


class IncludeManyToMany(BadiFilterBase, filters.CharFilter):
    def filter(self, qs, value):
        if len(value) > 0 and value not in ['null', None]:
            return qs.filter(**{self.field_name: value})
        else:
            return qs


class BadiTextListInFilter(BadiFilterBase, filters.MultipleChoiceFilter):

    def filter(self, qs, value):
        for x in self.parent.form.data.getlist(self.field_name + '[]'):
            qs = qs.filter(**{self.field_name + '__in': x})
        return qs


class BadiFullNameTextIn(BadiFilterBase, filters.CharFilter):
    def filter(self, qs, value):
        if len(value) > 0:
            return qs.annotate(full_name=Concat('first_name', Value(' '), 'last_name')). \
                filter(Q(**{self.field_name + '__icontains': value}) | Q(full_name__icontains=value))
        else:
            return qs


class UserListFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
            'is_admin',
        ]

    username = TextIn(field_name='username')
    first_name = TextIn(field_name='first_name')
    last_name = TextIn(field_name='last_name')
    mobile_number = TextIn(field_name='mobile_number')


class MemberListFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
        ]

    username = TextIn(field_name='username')
    first_name = TextIn(field_name='first_name')
    last_name = TextIn(field_name='last_name')
    mobile_number = TextIn(field_name='mobile_number')
