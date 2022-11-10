from django.contrib.auth.models import Group

from badi_utils.dynamic import DynamicCreateView, DynamicUpdateView
from badi_utils.utils import dynamic_permision


class RoleCreateView(DynamicCreateView):
    permission_required = 'user.can_group'
    model = Group
    extra_context = {
        'permissions': dynamic_permision()
    }
    api_url = '/api/v1/group/'


class RoleUpdateView(DynamicUpdateView):
    permission_required = 'user.can_group'
    model = Group
    extra_context = {
        'permissions': dynamic_permision()
    }
    api_url = '/api/v1/group/'
