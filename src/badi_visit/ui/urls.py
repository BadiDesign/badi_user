from badi_utils.dynamic import *
from badi_blog.ui.views import *
from badi_visit.models import RedirectUrl
from badi_visit.ui.views import RedirectUrlCreateView, RedirectUrlUpdateView

redirect_urls = multi_generator_url(RedirectUrl(), create=RedirectUrlCreateView, update=RedirectUrlUpdateView)
urlpatterns = [
              ] + redirect_urls
