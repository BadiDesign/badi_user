from badi_utils.sms import IpPanelSms
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse, Http404
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from django.utils.translation import gettext_lazy as _
from badi_utils.dynamic_api import DynamicModelApi, CustomValidation
from badi_utils.responses import ResponseOk
from badi_utils.date_calc import custom_change_date
from badi_ticket.models import Ticket, Message
from badi_ticket.serializers import TicketCreateSerializer, MessageCreateSerializer
from badi_user.filter import MemberListFilter
from django.contrib.auth import get_user_model

User = get_user_model()
BADI_AUTH_CONFIG = getattr(settings, "BADI_AUTH_CONFIG", {})


def send_ticket(user, message_title, message_text, sender):
    count = 0
    for user in user:
        ticket, is_created = Ticket.objects.get_or_create(user=user, title=message_title)
        message = Message(ticket=ticket, text=message_text, user=sender)
        message.save()
        count += 1

    return count


def send_sms(users, message_title, message_text, sender):
    count = 0
    for user in users:
        ticket, is_created = Ticket.objects.get_or_create(user=user, title=message_title)
        message = Message(ticket=ticket, text=message_text, user=sender)
        message.save()
        count += 1

    BADI_AUTH_CONFIG.get('sms').get('sms_panel').board_send(users, message_text)
    return count


class TicketViewSet(DynamicModelApi):
    columns = ['id', 'writer', 'title', 'is_closed', 'created_at', ]
    order_columns = ['id', 'writer', 'title', 'is_closed', 'created_at', ]
    model = Ticket
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    custom_perms = {
        'datatable': True,
        'create': True,
    }

    def render_column(self, row, column):
        if column == 'is_closed':
            if self.request.user.is_admin:
                count = row.messages.filter(is_seen_by_admin=False).count()
            else:
                count = row.messages.filter(is_seen=False).count()
            first = row.messages.all().order_by('-pk').first()
            last_message = -1
            if first:
                if first.writer.is_admin:
                    last_message = 1
                else:
                    last_message = 0
            return [row.is_closed, count, last_message]
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        if self.request.user.is_member():
            return Ticket.objects.filter(writer=self.request.user)
        return super().filter_queryset(qs)

    def get_queryset(self):
        if self.request.user.is_member():
            return Ticket.objects.filter(writer=self.request.user)
        return self.queryset

    @action(methods=['post'], detail=False)
    def send_ticket(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            selected = request.data.get('selected')
            exclude = request.data.get('exclude')
            is_all_select = request.data.get('is_all_select')
            message_title = request.data.get('message_title')
            message_text = request.data.get('message_text')
            if not message_title or not message_text:
                return JsonResponse({
                    'message': _("Please fill title and text fields"),
                    'done': False
                })

            qs = User.objects.none()
            if is_all_select is True:
                qs = MemberListFilter(self.request.data).qs.filter(is_admin=False)
                if exclude:
                    qs = qs.exclude(id__in=exclude)
            elif selected:
                qs = User.objects.filter(id__in=selected)
            if qs.exists():
                count = send_ticket(qs, message_title, message_text, self.request.user)
                if count == 0:
                    text_res = _('SomeThing Happened! No message sent!')
                    return JsonResponse({
                        'message': text_res,
                        'done': False
                    })
                else:
                    text_res = _('Your Ticket and Message sent to #0 User successfully!')
                    return JsonResponse({
                        'message': text_res.replace("#0", str(count)),
                        'done': True
                    })
            else:
                return JsonResponse({
                    'message': _('Select a member!'),
                    'done': False
                })
        raise CustomValidation('ticket', _('You dont have permission to Send Ticket!'))

    @action(methods=['post'], detail=False)
    def send_sms(self, request, *args, **kwargs):
        if self.request.user.is_admin:
            selected = request.data.get('selected')
            exclude = request.data.get('exclude')
            is_all_select = request.data.get('is_all_select')
            message_title = "پیامک"
            message_text = request.data.get('message_text')
            if not message_title or not message_text:
                return JsonResponse({
                    'message': _("Please fill title and text fields"),
                    'done': False
                })

            qs = User.objects.none()
            if is_all_select is True:
                qs = MemberListFilter(self.request.data).qs.filter(is_admin=False)
                if exclude:
                    qs = qs.exclude(id__in=exclude)
            elif selected:
                qs = User.objects.filter(id__in=selected)
            if qs.exists():
                count = send_sms(qs, message_title, message_text, self.request.user)
                if count == 0:
                    text_res = _('SomeThing Happened! No message sent!')
                    return JsonResponse({
                        'message': text_res,
                        'done': False
                    })
                else:
                    text_res = _('Your Ticket and Message sent to #0 User successfully!')
                    return JsonResponse({
                        'message': text_res.replace("#0", str(count)),
                        'done': True
                    })
            else:
                return JsonResponse({
                    'message': _('Select a member!'),
                    'done': False
                })
        raise CustomValidation('ticket', _('You dont have permission to Send Ticket!'))

    @action(methods=['post'], detail=False)
    def create_ticket_mobile(self, request, *args, **kwargs):
        title = self.request.data.get('title')
        if self.request.user.is_admin:
            user = self.request.data.get('user')
            Ticket(user=user, title=title).save()
            return ResponseOk()
        else:
            Ticket(user=self.request.user, title=title).save()
            return ResponseOk()

    @action(methods=['get'], detail=False)
    def select2(self, request, *args, **kwargs):
        request_get = request._request.GET
        page = request_get.get('page', 1)
        search = request_get.get('search')
        thing = User.objects.all()
        if search is not None and len(search.strip()) > 0:
            thing = thing.filter(**{self.text + '__contains': search})
        paginator = Paginator(thing, 10)
        results = paginator.page(int(page)).object_list
        results_bitten = results
        results_bitten = [{'id': x.id, 'text': x.__str__()} for x in results_bitten]
        return JsonResponse({
            'results': results_bitten,
            "pagination": {
                "more": paginator.page(page).has_next()
            }
        }, safe=False)


class MessageViewSet(DynamicModelApi):
    columns = ['id', 'ticket', 'text', 'user', 'file', 'is_seen', 'is_seen_by_admin', 'created_at', ]
    order_columns = ['id', 'ticket', 'text', 'user', 'file', 'is_seen', 'is_seen_by_admin', 'created_at', ]
    model = Message
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    custom_perms = {
        'list': True,
        'ticket': True,
        'create': True,
    }

    @action(methods=['get'], detail=False, url_path='ticket/(?P<pk>[^/.]+)')
    def ticket(self, request, pk, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=pk)
        user = self.request.user
        if ticket.writer != user and user.is_member():
            raise Http404()
        messages = ticket.messages.all().order_by('pk')
        if user.is_member():
            messages.update(is_seen=True)
        if user.is_admin:
            messages.update(is_seen_by_admin=True)
        res = [
            {
                'pk': msg.pk, 'text': msg.text,
                'is_admin': False if msg.writer.is_member() else True,
                'file': msg.file.url if msg.file else None,
                'is_seen': msg.is_seen, 'is_seen_by_admin': msg.is_seen_by_admin,
                'created_at': custom_change_date(msg.created_at, 4),
            } for msg in messages
        ]
        return JsonResponse({'response': res, 'ticket': {
            'fullname': ticket.writer.get_full_name(),
            'title': ticket.title,
            'is_closed': ticket.is_closed,
            'created_at': custom_change_date(ticket.created_at, 4),
        }})

    def filter_queryset(self, qs):
        return super().filter_queryset(qs)

    def get_queryset(self):
        return self.queryset
