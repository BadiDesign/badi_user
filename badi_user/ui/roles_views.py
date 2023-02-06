from django.contrib.auth.models import Group

from badi_utils.dynamic import DynamicCreateView, DynamicUpdateView
from badi_utils.utils import permissions_json


class RoleCreateView(DynamicCreateView):
    permission_required = 'user.can_group'
    model = Group
    datatable_cols = ['id', 'name', 'permissions']
    extra_context = {
        'permissions': permissions_json()
    }
    api_url = '/api/v1/group/'


class RoleUpdateView(DynamicUpdateView):
    permission_required = 'user.can_group'
    model = Group
    extra_context = {
        'permissions': permissions_json()
    }
    api_url = '/api/v1/group/'
