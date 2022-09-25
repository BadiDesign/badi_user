from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_user.filter import UserListFilter
from django.contrib.auth import get_user_model

User = get_user_model()

from badi_user.ui.forms import user_form


class MemberListView(DynamicListView):
    model = User
    model_name = 'عضو'
    datatable_cols = ['#', "انتخاب", 'تصویر', 'نام کاربری', 'نام', 'نام خانوادگی', 'موجودی کیف پول']
    template_name = 'member/member_list.html'

    def get_extra_context(self, context):
        context['filters'] = UserListFilter(self.request.POST)
        return super().get_extra_context(context)


class MemberCreateView(DynamicCreateView):
    model = User
    model_name = 'عضو'
    form = user_form(User.get_form_fields('member_create'))
    template_name = 'member/member_create.html'
    datatableEnable = False

    def get_extra_context(self, context):
        context['back'] = '/user/member/list'
        return context


class MemberUpdateView(DynamicUpdateView):
    model = User
    model_name = 'عضو'
    form = user_form(
        ['username', 'password', 'first_name', 'last_name', 'is_admin', 'mobile_number', 'picture', ], update=True)
    success_url = '/user/member/list'
    template_name = 'member/member_update.html'


class MemberSelfUpdateView(DynamicUpdateView):
    model = User
    model_name = 'عضو'
    form = user_form(User.get_form_fields('member_create'), update=True)
    success_url = '/user/member/list'
    template_name = 'member/member_self_update.html'

    def get_object(self, queryset=None):
        return self.request.user
