from plugins.dynamic import *
from .views import *

urlpatterns = [
    path('ticket/create', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/list', TicketCreateView.as_view(), name='ticket_list'),
    path('ticket/update/<int:pk>', TicketUpdateView.as_view(), name='ticket_update'),
    path('ticket/messages/<int:pk>', MessageListView.as_view(), name='ticket_messages'),

    path('message/create/<int:pk>', MessageCreateView.as_view(), name='message_create'),
    path('message/list/<int:pk>', MessageListView.as_view(), name='message_list'),
]
