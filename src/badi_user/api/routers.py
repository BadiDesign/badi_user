from badi_user.api.api import UserViewSet, AuthViewSet, GroupViewSet, MemberViewSet, LogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('member', MemberViewSet, basename='member')
router.register('group', GroupViewSet, basename='group')
router.register('auth', AuthViewSet, basename='auth')
router.register('log', LogViewSet, basename='log')

urlpatterns = router.urls
