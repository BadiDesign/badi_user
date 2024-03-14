from badi_visit.api.api import VisitViewSet, AddressVisitViewSet, RedirectUrlViewSet, SearchQueryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('visit', VisitViewSet, basename='visit')
router.register('addressvisit', AddressVisitViewSet, basename='addressvisit')
router.register('redirecturl', RedirectUrlViewSet, basename='redirecturl')
router.register('searchquery', SearchQueryViewSet, basename='searchquery')
urlpatterns = router.urls
