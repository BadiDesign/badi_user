from datetime import timedelta, datetime

from badi_utils.dynamic_models import BadiModel
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from badi_utils.utils import get_client_ip


class AddressVisit(models.Model, BadiModel):
    class Meta:
        verbose_name = 'Address Visit'
        verbose_name_plural = 'Address Visits'
        permissions = (
            # ('can_address', 'Manage Address Visit'),
        )
        ordering = ('-visitors_count',)

    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Address')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Title')
    visits_count = models.IntegerField(default=0, verbose_name='Visits count')
    visitors_count = models.IntegerField(default=0, verbose_name='Visitors count')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')

    def __str__(self):
        return self.title if self.title else self.address

    def get_count(self):
        return self.visits.all().count()

    def update_visits(self):
        self.visits_count = self.visits.count()
        self.visitors_count = len(set(self.visits.all().values_list('ip', flat=True)))
        self.save()


class Visit(models.Model):
    class Meta:
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'
        permissions = (
            ('can_visit', 'Manage Visit'),
        )

    address = models.ForeignKey(AddressVisit, blank=True, verbose_name='Address', related_name='visits',
                                on_delete=models.CASCADE)
    ip = models.CharField(max_length=200, verbose_name='ip')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Visit Time')

    def __str__(self):
        return f'{self.ip} - {self.address.__str__()}'

    @staticmethod
    def visit(request, title):
        visit = Visit()
        visit.ip = get_client_ip(request)
        visit.address, is_created = AddressVisit.objects.get_or_create(title=title, )
        if is_created or not visit.address.address:
            visit.address.address = request.path
            visit.address.save()
        visit.save()
        return visit

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.address.updated_at or self.address.updated_at < (datetime.now() - timedelta(minutes=1)):
            self.address.update_visits()
