from badi_utils.dynamic import DynamicListView
from badi_user.filter import LogFilter
from badi_user.models import Log


class LogListView(DynamicListView):
    model = Log
    deleteShow = False
    editShow = False
    api_url = '/api/v1/log/'
    extra_context = {
        'form': LogFilter().form
    }
