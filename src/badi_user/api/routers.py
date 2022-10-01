from badi_user.api.api import UserViewSet, AuthViewSet, GroupViewSet, MemberViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('member', MemberViewSet, basename='member')
router.register('group', GroupViewSet, basename='group')
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
