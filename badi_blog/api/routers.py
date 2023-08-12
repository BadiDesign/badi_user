from badi_blog.api.api import BlogPostViewSet, CommentViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('blogpost', BlogPostViewSet, basename='blogpost')
router.register('comment', CommentViewSet, basename='comment')

urlpatterns = router.urls
