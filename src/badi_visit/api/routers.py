from badi_visit.api.api import VisitViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('visit', VisitViewSet, basename='visit')
urlpatterns = router.urls
