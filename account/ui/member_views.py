from badi_utils.dynamic import DynamicListView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from account.filter import CustomMemberFilter

User = get_user_model()


class CustomMemberListView(DynamicListView):
    model = User
    model_name = _('Member')
    datatable_cols = User.get_datatable_cols('MemberListView')
    template_name = 'member/member_list.html'
    api_url = '/api/v1/member/'

    def get_extra_context(self, context):
        context['filters'] = CustomMemberFilter(self.request.POST)
        return super().get_extra_context(context)
