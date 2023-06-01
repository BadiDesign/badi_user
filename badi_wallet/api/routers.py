from rest_framework.routers import DefaultRouter
from badi_wallet.api.view_sets import TransactionViewSet, DiscountCodeViewSet

router = DefaultRouter()
router.register('transaction', TransactionViewSet, basename='transaction')
router.register('discountcode', DiscountCodeViewSet, basename='discountcode')
urlpatterns = router.urls
