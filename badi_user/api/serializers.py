from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from badi_utils.dynamic_api import api_error_creator, DynamicSerializer
from badi_user.models import Notification, Log
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(DynamicSerializer):
    class Meta:
        model = User
        fields = User.get_form_fields('profile')


class UserRegisterSerializer(DynamicSerializer):
    class Meta:
        model = User
        fields = User.get_form_fields('register')


class UserSerializer(DynamicSerializer):
    remove_field_view = User.get_remove_fields('UserSerializer') if hasattr(User, 'remove_field_view') else {
        'retrieve': ['password', ],
        'update_self': ['mobile_number', ],
        'self': ['password', ]
    }

    class Meta:
        model = User
        extra_kwargs = api_error_creator(User, User.get_form_fields('UserSerializer'),
                                         blank_fields=['username', 'password'],
                                         required_fields=['first_name', 'last_name',
                                                          'mobile_number'])
        depth = 5
        fields = ['id', ] + User.get_form_fields('UserSerializer')

    def create(self, validated_data):
        validated_data['is_admin'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_password(self, value):
        if self.context['view'].action == 'create':
            data = self.get_initial()
            password = data.get('password')
            if password is None or password == '':
                raise serializers.ValidationError('رمز عبور باید وارد شود')

        return make_password(value)

    def validate_mobile_number(self, value):
        if self.context['view'].action == 'create':
            data = self.get_initial()
            if value is None or value == '':
                raise serializers.ValidationError('شماره همراه باید وارد شود')
        return value


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = api_error_creator(User, ['username', 'first_name', 'last_name', 'mobile_number', 'password'],
                                         required_fields=[])
        fields = ['username', 'first_name', 'last_name', 'mobile_number', 'password']

    def validate_password(self, value):
        data = self.get_initial()
        password = value
        password = data.get('password')
        if password is None or password == '':
            raise serializers.ValidationError('رمز عبور باید وارد شود')
        return value


class MemberSerializer(DynamicSerializer):
    remove_field_view = User.get_remove_fields('MemberSerializer') if hasattr(User, 'remove_field_view') else {
        'retrieve': ['password', ],
        'update_self': ['password', 'username', 'mobile_number', 'amount'],
        'update': ['password', 'amount'],
        'self': ['password', ],
    }

    class Meta:
        model = User
        extra_kwargs = api_error_creator(User,
                                         ['username', 'first_name', 'last_name', 'picture', 'password'],
                                         required_fields=['first_name', 'last_name', 'mobile_number'])
        depth = 5
        fields = ['id', 'username', 'first_name', 'last_name', 'mobile_number', 'picture', 'password', 'amount']

    def create(self, validated_data):
        validated_data['is_admin'] = False
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_password(self, value):
        if self.context['view'].action == 'create':
            data = self.get_initial()
            password = data.get('password')
            if password is None or password == '':
                raise serializers.ValidationError('رمز عبور باید وارد شود')

        return make_password(value)

    def validate_mobile_number(self, value):
        if self.context['view'].action == 'create':
            data = self.get_initial()
            if value is None or value == '':
                raise serializers.ValidationError('شماره همراه باید وارد شود')
        return value


class GroupSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Group
        extra_kwargs = api_error_creator(Group,
                                         ['name', 'permissions'],
                                         required_fields=['name', 'permissions'])
        depth = 5
        fields = ['id', 'name', 'permissions']


class NotificationSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Notification
        extra_kwargs = api_error_creator(Notification,
                                         ['user', 'subject', 'text', 'show_date', 'is_seen', ],
                                         required_fields=['user', 'subject', 'text', 'show_date', 'is_seen', ])
        depth = 5
        fields = ['id', 'user', 'subject', 'text', 'show_date', 'is_seen', ]


class LogSerializer(DynamicSerializer):
    remove_field_view = {
    }

    class Meta:
        model = Log
        extra_kwargs = api_error_creator(Log,
                                         Log.get_serializer_fields(),
                                         required_fields=Log.get_serializer_fields())
        depth = 5
        fields = ['id', ] + Log.get_serializer_fields()
