from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_ticket.models import Message, Ticket
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TicketListView(DynamicListView):
    # permission_required = ROLES_ADMIN_TEACHER
    permission_required = True
    model = Ticket
    datatable_cols = ['#', _('Member'), _('Title'), _('Category'), _('Status'), _("Created at")]


class TicketCreateView(DynamicCreateView):
    model = Ticket
    success_url = '/ticket/ticket/list'
    permission_required = True
    datatable_cols = ['#', _('Member'), _('Title'), _('Category'), _('Status'), _("Created at")]
    # permission_required = ROLES_ADMIN_TEACHER
    form_fields = ['title', 'writer', 'category']

    # updateURL = '/ticket/ticket/update/0'

    def get_extra_context(self, context):
        context['form'].fields['writer'].queryset = User.objects.none()
        return super().get_extra_context(context)


class TicketUpdateView(DynamicUpdateView):
    model = Ticket
    success_url = '/dashboard/ticket/ticket/list'
    form_fields = ['title', 'writer', 'is_closed']

    def get_extra_context(self, context):
        context['form'].fields['writer'].queryset = User.objects.none()
        context['api_url'] = '/api/v1/ticket/'
        context['successURL'] = self.success_url
        return super().get_extra_context(context)


class MessageListView(DynamicListView):
    # permission_required = ROLES_ADMIN_TEACHER
    template_name = 'ticket/message_list.html'
    permission_required = True
    model = Message
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'نقش']

    def get_extra_context(self, context):
        context['pk'] = self.kwargs['pk']
        return super().get_extra_context(context)


class MessageCreateView(DynamicCreateView):
    model = Message
    success_url = '/message/list'
    datatableEnable = False
    permission_required = True
