from random import choices

from django.utils.deconstruct import deconstructible

from badi_utils.dynamic_models import BadiModel
from django.core.validators import MaxLengthValidator, BaseValidator
from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _, ngettext_lazy
from django.contrib.auth import get_user_model

User = get_user_model()


@deconstructible
class MaxFileLengthValidator(BaseValidator):
    message = ngettext_lazy(_('File must be less than %(limit_value)d mb!'),
                            _('File must be less than %(limit_value)d mb!'),
                            'limit_value',
                            )
    code = 'max_size'

    def compare(self, a, b):
        return a > (b * 1024 * 1024)

    def clean(self, x):
        return x.size if x else 0


def file_size(value):  # add this to some file where you can import it from
    limit = 1 * 1024 * 1024
    try:
        if value and value.size > limit:
            raise ValidationError(_('File must be less than 1 mb!'))
    except:
        print(value.url + ' NOT FOUND!!!')


class Ticket(models.Model, BadiModel):
    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Ticket')
        permissions = (
            ('can_ticket', _('Manage Tickets')),
        )

    TICKET_CHOICES = (
        ('sell', _('Sell')),
        ('public_question', _('Public question')),
        ('technical_question', _('Technical question')),
        ('authentication', _('Authentication')),
        ('complaint', _('Complaint')),
        ('financial', _('Financial')),
        ('other', _('Other')),
    )
    writer = models.ForeignKey(User, null=True, related_name='tickets', on_delete=models.CASCADE,
                               verbose_name=_('Member'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    category = models.CharField(max_length=50, choices=TICKET_CHOICES, default="public_question", )
    is_closed = models.BooleanField(default=False, verbose_name=_('is Closed'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Created at"))

    def __str__(self):
        return self.title + ' (' + self.writer.__str__() + ')'

    def unread_count(self, user=None):
        count = 0
        if user.is_admin:
            count = self.messages.filter(is_seen_by_admin=False).count()
        else:
            count = self.messages.filter(is_seen=False).count()
        return count

    def unread_messages(self, user):
        if user.is_admin:
            return self.messages.filter(is_seen_by_admin=False)
        else:
            return self.messages.filter(is_seen=False)

    @staticmethod
    def unread_messages_of(user):
        unread = 0
        if not user.is_authenticated:
            return 0
        if user.is_admin:
            for tkt in Ticket.objects.all():
                unread += tkt.messages.filter(is_seen_by_admin=False).count()
        else:
            for tkt in user.tickets.all():
                unread += tkt.messages.filter(is_seen=False).count()
        return unread


class Message(models.Model, BadiModel):
    class Meta:
        permissions = (
            ('can_ticket', _('Manage Tickets')),
        )
        ordering = ['-created_at']

    tickt = models.ForeignKey(Ticket, related_name='messages', null=True, on_delete=models.CASCADE,
                              verbose_name=_("Ticket"))
    text = models.TextField(verbose_name=_("Message Text"), validators=[MaxLengthValidator(400)])
    writer = models.ForeignKey(User, related_name='messages', null=True, on_delete=models.CASCADE,
                               verbose_name=_("Writer"))
    file = models.FileField(upload_to='messages/', blank=True, null=True, verbose_name=_("File"),
                            validators=[MaxFileLengthValidator(1)])
    is_seen = models.BooleanField(default=False, verbose_name=_("Is seen by user"))
    is_seen_by_admin = models.BooleanField(default=False, verbose_name=_("Is seen by admin"))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Sent at"))

    def __str__(self):
        return self.tickt.title + ' - ' + self.writer.__str__()
