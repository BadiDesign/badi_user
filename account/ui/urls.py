from badi_utils.dynamic import *
from account.ui.member_views import *

urlpatterns = [
    path('member/list', CustomMemberListView.as_view(), name='member_list'),
]
