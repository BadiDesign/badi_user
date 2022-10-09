from badi_ticket.api import TicketViewSet, MessageViewSet
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ticket', TicketViewSet, basename='ticket')
router.register('message', MessageViewSet, basename='message')
urlpatterns = router.urls
