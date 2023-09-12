from badi_visit.api.api import VisitViewSet, AddressVisitViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('visit', VisitViewSet, basename='visit')
router.register('addressvisit', AddressVisitViewSet, basename='addressvisit')
urlpatterns = router.urls
