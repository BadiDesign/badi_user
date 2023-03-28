from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_user.filter import UserListFilter, MemberListFilter
from django.contrib.auth import get_user_model
from badi_user.ui.forms import user_form
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class MemberListView(DynamicListView):
    model = User
    model_name = _('Member')
    api_url = '/api/v1/member/'
    datatable_cols = User.get_datatable_cols('MemberListView')
    template_name = 'member/member_list.html'

    def get_extra_context(self, context):
        context['filters'] = MemberListFilter(self.request.POST)
        return super().get_extra_context(context)


class MemberCreateView(DynamicCreateView):
    model = User
    model_name = _('Member')
    api_url = '/api/v1/member/'
    form = user_form(User.get_form_fields('member_create'))
    template_name = 'member/member_create.html'
    datatableEnable = False

    def get_extra_context(self, context):
        context['back'] = '/user/member/list'
        return context


class MemberUpdateView(DynamicUpdateView):
    model = User
    model_name = _('Member')
    api_url = '/api/v1/member/'
    form = user_form(User.get_form_fields('member_update'), update=True)
    template_name = 'member/member_update.html'


class MemberSelfUpdateView(DynamicUpdateView):
    model = User
    model_name = _('Member')
    form = user_form(User.get_form_fields('member_self_update'), update=True)
    success_url = '/user/member/list'
    template_name = 'member/member_self_update.html'

    def get_object(self, queryset=None):
        return self.request.user
