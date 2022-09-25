from badi_utils.dynamic import *
from badi_user.ui.member_views import *
from badi_user.ui.views import *
from django.contrib.auth import get_user_model

User = get_user_model()
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='custom_login'),
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
