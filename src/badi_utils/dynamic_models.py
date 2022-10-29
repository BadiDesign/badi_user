import re

from django.contrib import admin
from django.contrib.sites import apps
from django.core import exceptions
from django.db import models
from django.db.models import Model

from .date_calc import custom_change_date

pattern_date = re.compile(r'(\d+/\d+/\d+)')
pattern_datetime = re.compile(r'(\d+/\d+/\d+)')


class BadiModel:
    def get_all_fields(self, excludes=None):
        if excludes is None:
            excludes = []
        fields = [field.attname.replace('_id', '') for field in self._meta.fields]
        many_2_many = [x.name for x in self._meta.many_to_many]
        all_fields = fields + many_2_many
        for f in all_fields:
            if f in excludes:
                all_fields.remove(f)
        return all_fields

    def get_columns(self, excludes=None):
        return self.get_all_fields(excludes)

    def get_datatable_columns(self, excludes=None):
        if excludes is None:
            excludes = []
        return self.get_all_fields(excludes)

    def get_datatable_verbose_names(self, excludes=None):
        if excludes is None:
            excludes = []
        fields = [field.verbose_name for field in self._meta.fields]
        many_2_many = [x.verbose_name for x in self._meta.many_to_many]
        all_fields = fields + many_2_many
        for f in all_fields:
            if f in excludes:
                all_fields.remove(f)
        return all_fields


class PersianDateField(models.DateField):

    def to_python(self, value):

        if value is None:
            return value
        if type(value) is str:
            try:
                if pattern_date.match(value):
                    value = custom_change_date(value, 6).strftime('%Y-%m-%d')
                else:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid'],
                        code='invalid',
                        params={'value': value},
                    )
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_date'],
                    code='invalid_date',
                    params={'value': value},
                )

        return super().to_python(value)


class PersianDateTimeField(models.DateTimeField):

    def to_python(self, value):

        if value is None:
            return value
        if type(value) is str:
            try:
                if pattern_datetime.match(value):
                    value = custom_change_date(value, 3)
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    raise exceptions.ValidationError(
                        self.error_messages['invalid'],
                        code='invalid',
                        params={'value': value},
                    )
            except ValueError:
                raise exceptions.ValidationError(
                    self.error_messages['invalid_date'],
                    code='invalid_date',
                    params={'value': value},
                )

        return super().to_python(value)


def get_app_models(module):
    return apps.get_app_config(module).models.items()


def set_admin(module):
    for key, model in get_app_models(module):
        admin.site.register(model)
