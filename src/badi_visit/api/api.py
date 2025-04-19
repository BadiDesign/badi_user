import datetime

from badi_blog.api.api import CustomPagination
from badi_utils.decorators import badi_cache
from badi_visit.api.serializers import AddressVisitSerializer, RedirectUrlSerializer, SearchQuerySerializer
from django.db.models import Count
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from badi_visit.models import Visit, AddressVisit, RedirectUrl, SearchQuery

from badi_utils.dynamic_api import DynamicModelApi, ViewSetPermission


@badi_cache(key='get_all_visits')
def get_all_visits():
    data = {
        'chart': {
            'visit': [],
            'visitor': [],
            'label': [],
        },
        'info': {
            'today': {'visit': 0, 'visitor': 0},
            'yesterday': {'visit': 0, 'visitor': 0},
            'week': {'visit': 0, 'visitor': 0},
            'month': {'visit': 0, 'visitor': 0},
            'year': {'visit': 0, 'visitor': 0},
            'all': {'visit': 0, 'visitor': 0},
        }
    }

    today_start = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)

    for index in range(15):
        cache_key = '_day_ago_visit_index_' + str(index)
        index_day_cache_data = cache.get(cache_key)
        day = today_start - datetime.timedelta(days=index)
        if index_day_cache_data:
            visits = index_day_cache_data[0]
            visitors = index_day_cache_data[1]
        else:
            visits = Visit.objects.filter(created_at__date=day).count()
            visitors = Visit.objects.filter(created_at__date=day).values('ip').distinct().count()
            if index != 0:
                cache.set(cache_key, [visits, visitors], 60 * 60 * 6)

        data['chart']['visit'].append(visits)
        data['chart']['visitor'].append(visitors)
        if index == 0:
            data['info']['today']['visit'] = visits
            data['info']['today']['visitor'] = visitors
        elif index == 1:
            data['info']['yesterday']['visit'] = visits
            data['info']['yesterday']['visitor'] = visitors
        data['chart']['label'].append(day.strftime('%m/%d'))

    @badi_cache(key='_get_week_visits_count', timeout=60 * 60)
    def _get_week_visits_count():
        week = today_start - datetime.timedelta(days=7)
        week_objects = Visit.objects.filter(created_at__gte=week)
        return week_objects.count(), week_objects.values('ip').distinct().count()

    week_visits, week_visitors = _get_week_visits_count()
    data['info']['week']['visit'] = week_visits
    data['info']['week']['visitor'] = week_visitors

    @badi_cache(key='_get_month_visits_count', timeout=6 * 60 * 60)
    def _get_month_visits_count():
        month = today_start - datetime.timedelta(days=30)
        month_objects = Visit.objects.filter(created_at__gte=month)
        return month_objects.count(), month_objects.values('ip').distinct().count()

    month_visits, month_visitors = _get_month_visits_count()
    data['info']['month']['visit'] = month_visits
    data['info']['month']['visitor'] = month_visitors

    @badi_cache(key='_get_year_visits_count', timeout=12 * 60 * 60)
    def _get_year_visits_count():
        year = today_start - datetime.timedelta(days=365)
        year_visit_qs = Visit.objects.filter(created_at__gte=year)
        return year_visit_qs.count(), year_visit_qs.values('ip').distinct().count()

    year_visits, year_visitors = _get_year_visits_count()
    data['info']['year']['visit'] = year_visits
    data['info']['year']['visitor'] = year_visitors

    @badi_cache(key='_get_all_visits_count', timeout=24 * 60 * 60)
    def _get_all_visits_count():
        return Visit.objects.all().count(), Visit.objects.all().values('ip').distinct().count()

    all_visits, all_visitors = _get_all_visits_count()
    data['info']['all']['visit'] = all_visits
    data['info']['all']['visitor'] = all_visitors
    return data


class VisitViewSet(ViewSetPermission, viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    custom_perms = {
        'all': 'badi_visit.can_visit',
    }

    @action(methods=['get'], detail=False)
    def all(self, request, *args, **kwargs):
        data = get_all_visits()
        return JsonResponse(data)


class AddressVisitViewSet(DynamicModelApi):
    model = AddressVisit
    serializer_class = AddressVisitSerializer
    queryset = model.objects.all()
    pagination_class = CustomPagination
    custom_perms = {
        'list': 'badi_visit.can_visit',
    }


class RedirectUrlViewSet(DynamicModelApi):
    model = RedirectUrl
    serializer_class = RedirectUrlSerializer
    queryset = model.objects.all()
    pagination_class = CustomPagination
    custom_perms = {
        'list': 'badi_visit.can_redirect',
    }


class SearchQueryViewSet(DynamicModelApi):
    model = SearchQuery
    serializer_class = SearchQuerySerializer
    queryset = model.objects.all()
    pagination_class = CustomPagination
    custom_perms = {
        'list': 'badi_visit.can_redirect',
    }
