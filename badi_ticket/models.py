from badi_utils.dynamic_models import BadiModel
from django.core.validators import MaxLengthValidator
from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


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

    writer = models.ForeignKey(User, null=True, related_name='tickets', on_delete=models.CASCADE,
                               verbose_name=_('Member'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    is_closed = models.BooleanField(default=False, verbose_name=_('is Closed'))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Created at"))

    def __str__(self):
        return self.title + ' (' + self.writer.__str__() + ')'

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
                            validators=[file_size])
    is_seen = models.BooleanField(default=False, verbose_name=_("Is seen by user"))
    is_seen_by_admin = models.BooleanField(default=False, verbose_name=_("Is seen by admin"))
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name=_("Sent at"))

    def __str__(self):
        return self.tickt.title + ' - ' + self.writer.__str__()
