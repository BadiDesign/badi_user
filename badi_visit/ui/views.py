from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_blog.filter import *
from badi_blog.models import *
from badi_visit.models import RedirectUrl, SearchQuery


class RedirectUrlCreateView(DynamicCreateView):
    model = RedirectUrl


class RedirectUrlUpdateView(DynamicUpdateView):
    model = RedirectUrl


class SearchQueryCreateView(DynamicCreateView):
    model = SearchQuery


class SearchQueryUpdateView(DynamicUpdateView):
    model = SearchQuery
