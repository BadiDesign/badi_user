from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_blog.filter import *
from badi_blog.models import *
from badi_visit.models import RedirectUrl


class RedirectUrlCreateView(DynamicCreateView):
    model = RedirectUrl


class RedirectUrlUpdateView(DynamicUpdateView):
    model = RedirectUrl
