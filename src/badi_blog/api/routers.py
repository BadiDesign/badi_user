from badi_blog.api.api import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('blogpost', BlogPostViewSet, basename='blogpost')
router.register('blogcomment', BlogCommentViewSet, basename='blogcomment')
router.register('blogcategory', BlogCategoryViewSet, basename='blogcategory')
router.register('blogbanner', BlogBannerViewSet, basename='blogbanner')
router.register('blogpartner', BlogPartnerViewSet, basename='blogpartner')
router.register('blogimage', BlogImageViewSet, basename='blogimage')

urlpatterns = router.urls
