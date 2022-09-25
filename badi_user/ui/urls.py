from plugins.dynamic import *
from user.ui.member_views import *
from user.ui.views import *

urlpatterns = [
    generate_url(User(), create=UserCreateView, add_model_to_url=False),
    generate_url(User(), view=UserListView, add_model_to_url=False),
    # generate_url(User(), delete=UserDeleteView),
    generate_url(User(), update=UserUpdateView, add_model_to_url=False),
    path('change_password/', ChangePasswordViewTemplateView.as_view(), name='change_password'),
    path('member/list', MemberListView.as_view(), name='member_list'),
    path('member/create', MemberCreateView.as_view(), name='member_create'),
    path('member/update/<int:pk>', MemberUpdateView.as_view(), name='member_update'),
    path('member/update/self', MemberSelfUpdateView.as_view(), name='member_self'),
]
