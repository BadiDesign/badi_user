from badi_user.api.api import AuthViewSet, GroupViewSet, LogViewSet
from account.api.api import CustomMemberViewSet, CustomUserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', CustomUserViewSet, basename='user')
router.register('member', CustomMemberViewSet, basename='member')
router.register('group', GroupViewSet, basename='group')
router.register('auth', AuthViewSet, basename='auth')
router.register('log', LogViewSet, basename='log')

urlpatterns = router.urls
