from badi_utils.dynamic import *
from badi_blog.ui.views import *
from badi_visit.models import RedirectUrl, SearchQuery
from badi_visit.ui.views import RedirectUrlCreateView, RedirectUrlUpdateView, SearchQueryCreateView, \
    SearchQueryUpdateView

redirect_urls = multi_generator_url(RedirectUrl(), create=RedirectUrlCreateView, update=RedirectUrlUpdateView)
search_query_urls = multi_generator_url(SearchQuery(), create=SearchQueryCreateView, update=SearchQueryUpdateView)
urlpatterns = [
              ] + redirect_urls + search_query_urls
