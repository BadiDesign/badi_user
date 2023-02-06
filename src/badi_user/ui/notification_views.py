from django.contrib.auth.models import Group

from badi_utils.dynamic import DynamicCreateView, DynamicUpdateView, DynamicListView
from badi_utils.utils import permissions_json
from badi_user.models import Notification


class NotificationCreateView(DynamicCreateView):
    permission_required = 'user.can_notification'
    model = Notification
    api_url = '/api/v1/notification/'


class NotificationListView(DynamicListView):
    permission_required = 'user.can_notification'
    model = Notification
    datatable_cols = ['id', 'Subject', 'Groups', 'IsAccepted', 'UnRead', 'Read', 'Doing', 'Done', 'CreatedAt']
    api_url = '/api/v1/notification/'
