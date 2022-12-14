import datetime
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from badi_visit.models import Visit


class VisitViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    custom_perms = {
        'all': 'badi_visit.can_visit',
    }

    @action(methods=['get'], detail=False)
    def all(self, request, *args, **kwargs):
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
            day = today_start - datetime.timedelta(days=index)
            visits = Visit.objects.filter(created_at__date=day).count()
            visitors = Visit.objects.filter(created_at__date=day).values('ip').distinct().count()
            data['chart']['visit'].append(visits)
            data['chart']['visitor'].append(visitors)
            if index == 0:
                data['info']['today']['visit'] = visits
                data['info']['today']['visitor'] = visitors
            elif index == 1:
                data['info']['yesterday']['visit'] = visits
                data['info']['yesterday']['visitor'] = visitors
            data['chart']['label'].append(day.strftime('%m/%d'))

        week = today_start - datetime.timedelta(days=7)
        week_objects = Visit.objects.filter(created_at__gte=week)
        data['info']['week']['visit'] = week_objects.count()
        data['info']['week']['visitor'] = week_objects.values('ip').distinct().count()

        month = today_start - datetime.timedelta(days=30)
        month_objects = Visit.objects.filter(created_at__gte=month)
        data['info']['month']['visit'] = month_objects.count()
        data['info']['month']['visitor'] = month_objects.values('ip').distinct().count()

        year = today_start - datetime.timedelta(days=365)
        year_objects = Visit.objects.filter(created_at__gte=year)
        data['info']['year']['visit'] = year_objects.count()
        data['info']['year']['visitor'] = year_objects.values('ip').distinct().count()

        all_objects = Visit.objects.all()
        data['info']['all']['visit'] = all_objects.count()
        data['info']['all']['visitor'] = all_objects.values('ip').distinct().count()
        return JsonResponse(data)
