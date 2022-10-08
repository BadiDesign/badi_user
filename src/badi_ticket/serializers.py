from plugins.dynamic_api import api_error_creator, CustomValidation
from plugins.dynamic_api import DynamicSerializer
from badi_ticket.models import Ticket, Message


class TicketCreateSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Ticket
        extra_kwargs = api_error_creator(Ticket,
                                         ['writer', 'title', 'created_at', 'is_closed', ],
                                         blank_fields=['writer'],
                                         required_fields=[])
        depth = 5
        fields = ['id', 'writer', 'title', 'created_at', 'is_closed', ]

    def create(self, validated_data):
        creator = self.context['request'].user
        if creator.is_member():
            validated_data['writer'] = creator
        validated_data['is_closed'] = False
        return super().create(validated_data)


class MessageCreateSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Message
        extra_kwargs = api_error_creator(Message,
                                         ['tickt', 'text', 'writer', 'file', 'is_seen', 'is_seen_by_admin',
                                          'created_at', ],
                                         blank_fields=['writer', 'file'],
                                         required_fields=['tickt'])
        depth = 5
        fields = ['id', 'tickt', 'text', 'writer', 'file', 'is_seen', 'is_seen_by_admin', 'created_at', ]

    def create(self, validated_data):
        writer = self.context['request'].user
        if validated_data['tickt'].writer != writer and writer.is_member():
            raise CustomValidation('tickt', 'شما اجازه ارسال پیام در این تیکت را ندارید!')
        validated_data['writer'] = writer
        if writer.is_member():
            validated_data['is_seen'] = True
        else:
            validated_data['is_seen_by_admin'] = True
        return super().create(validated_data)
