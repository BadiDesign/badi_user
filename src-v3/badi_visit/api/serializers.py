import datetime

from badi_visit.models import AddressVisit, RedirectUrl, SearchQuery
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from badi_utils.dynamic_api import api_error_creator, DynamicSerializer
from django.contrib.auth import get_user_model


class AddressVisitSerializer(DynamicSerializer):
    today_visit = serializers.SerializerMethodField()
    today_visitor = serializers.SerializerMethodField()

    class Meta:
        model = AddressVisit
        fields = ['id', 'address', 'title', 'today_visit', 'visits_count', 'today_visitor', 'visitors_count', ]

    def get_today_visit(self, obj):
        start_of_day = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
        return obj.visits.filter(created_at__gt=start_of_day).count()

    def get_today_visitor(self, obj):
        start_of_day = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
        return len(set(obj.visits.filter(created_at__gt=start_of_day).values_list('ip', flat=True)))


class RedirectUrlSerializer(DynamicSerializer):
    class Meta:
        model = RedirectUrl
        extra_kwargs = api_error_creator(model, model().get_all_fields())
        fields = model().get_all_fields()


class SearchQuerySerializer(DynamicSerializer):
    class Meta:
        model = SearchQuery
        extra_kwargs = api_error_creator(model, model().get_all_fields())
        fields = model().get_all_fields()
