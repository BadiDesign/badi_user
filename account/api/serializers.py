from badi_user.api.serializers import MemberSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from badi_utils.dynamic_api import api_error_creator, DynamicSerializer, CustomValidation
from badi_user.models import Notification, Log
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(DynamicSerializer):
    remove_field_view = {
        'retrieve': ['password', ],
        'update_self': ['mobile_number', ],
        'self': ['password', ]
    }

    class Meta:
        model = User
        extra_kwargs = api_error_creator(User,
                                         ['username', 'password', 'picture', 'first_name', 'last_name', 'mobile_number',
                                          'picture', ],
                                         blank_fields=['username', 'password'],
                                         required_fields=['first_name', 'last_name',
                                                          'mobile_number'])
        depth = 5
        fields = ['id', 'username', 'password', 'picture', 'first_name', 'last_name', 'mobile_number',
                  'is_admin', 'mobile_number',
                  ]

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


class CustomMemberSerializer(MemberSerializer):
    remove_field_view = {
        'retrieve': ['password', ],
        'update_self': ['password', 'username', 'mobile_number', 'amount', 'level', 'level_expired', 'national_code',
                        'call_number', ],
        'update': ['password', 'amount'],
        'self': ['password', ],
        'create': ['username'],
    }

    class Meta:
        model = User
        extra_kwargs = api_error_creator(User,
                                         ['first_name', 'last_name', 'picture', 'password', 'level', 'level_expired', ],
                                         required_fields=['first_name', 'last_name', 'mobile_number'],
                                         blank_fields=[])
        depth = 1
        fields = ['id', 'first_name', 'last_name', 'mobile_number', 'national_code', 'picture', 'password', 'level',
                  'city', 'plaque', 'title', 'call_number',
                  'address', 'level_expired', ]

    def create(self, validated_data):
        validated_data['is_admin'] = False
        validated_data['username'] = validated_data['national_code']
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
