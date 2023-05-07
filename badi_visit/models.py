from datetime import timedelta, datetime
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from badi_utils.utils import get_client_ip


class AddressVisit(models.Model):
    class Meta:
        verbose_name = 'Address Visit'
        verbose_name_plural = 'Address Visits'
        permissions = (
            # ('can_address', 'Manage Address Visit'),
        )

    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Address')
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Title')

    def __str__(self):
        return self.title if self.title else self.address

    def get_count(self):
        return self.visits.all().count()


class Visit(models.Model):
    class Meta:
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'
        permissions = (
            ('can_visit', 'Manage Visit'),
        )

    address = models.ForeignKey(AddressVisit, blank=True, verbose_name='Address', related_name='visits',
                                on_delete=models.PROTECT)
    ip = models.CharField(max_length=200, verbose_name='ip')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Visit Time')

    def __str__(self):
        return f'{self.ip} - {self.address.__str__()}'

    @staticmethod
    def visit(request, title):
        visit = Visit()
        visit.ip = get_client_ip(request)
        visit.address, is_created = AddressVisit.objects.get_or_create(title=title)
        visit.save()
        return visit
