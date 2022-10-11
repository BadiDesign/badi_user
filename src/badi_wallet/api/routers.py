from rest_framework.routers import DefaultRouter
from badi_wallet.api.view_sets import TransactionViewSet

router = DefaultRouter()
router.register('transaction', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
