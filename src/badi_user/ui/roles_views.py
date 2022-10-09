from django.contrib.auth.models import Group

from plugins.dynamic import DynamicCreateView, DynamicUpdateView
from plugins.utils import dynamic_permision


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
