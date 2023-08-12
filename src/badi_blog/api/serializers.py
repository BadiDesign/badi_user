from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from badi_utils.dynamic_api import api_error_creator, DynamicSerializer, CustomValidation
from badi_blog.models import *
from badi_utils.validations import PersianValidations


class BlogPostSerializer(DynamicSerializer):
    remove_field_view = {
        'create': ['writer', ],
        'update': ['writer', ],
    }

    class Meta:
        model = BlogPost
        extra_kwargs = api_error_creator(BlogPost,
                                         ['title', 'picture', 'slug', 'slider_title', 'slider_picture',
                                          'breaking_title', 'categories', 'is_recommend', 'short', 'description',
                                          'view', 'source_title', 'source_link', 'writer',
                                          ],
                                         blank_fields=[],
                                         required_fields=[])
        # depth = 1
        fields = ['title', 'picture', 'slug', 'slider_title', 'slider_picture',
                  'breaking_title', 'categories', 'is_recommend', 'short', 'description',
                  'view', 'source_title', 'source_link', 'writer',
                  ]

    def create(self, validated_data):
        validated_data['writer'] = self.context['request'].user
        tags = self.context['request'].data.getlist('tags', '')
        tag_ids = []
        for tag in tags:
            obj, is_created = BlogTag.objects.get_or_create(title=tag)
            tag_ids.append(obj.id)
        validated_data['tags'] = BlogTag.objects.filter(id__in=tag_ids)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        tags = self.context['request'].data.getlist('tags', '')
        tag_ids = []
        for tag in tags:
            obj, is_created = BlogTag.objects.get_or_create(title=tag)
            tag_ids.append(obj.id)
        validated_data['tags'] = BlogTag.objects.filter(id__in=tag_ids)
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


class BlogCommentSerializer(DynamicSerializer):
    remove_field_view = {
        'create': ['writer', 'replies', ],
        'update': ['writer', 'replies', ],
        'list': ['writer', 'writer_phone', 'film'],
    }
    replies = serializers.SerializerMethodField()

    class Meta:
        model = BlogComment
        extra_kwargs = api_error_creator(model, model.get_serializer_fields(),
                                         blank_fields=[],
                                         required_fields=['title'])
        fields = model.get_serializer_fields()
        depth = 1

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['writer'] = user
        if not PersianValidations.phone_number(validated_data['writer_phone']):
            raise CustomValidation('writer_phone', 'شماره تماس وارد شده صحیح نمی باشد.')
        if validated_data.get('replay') and validated_data['replay'].replay:
            raise CustomValidation('replay', 'شما نمی توانید به این نظر پاسخی ارسال کنید!')
        return super().create(validated_data)

    def get_replies(self, obj):
        return BlogCommentSerializer(instance=obj.replies.filter(is_accepted=True), many=True).data


class BlogCategorySerializer(DynamicSerializer):
    class Meta:
        model = BlogCategory
        extra_kwargs = api_error_creator(BlogCategory, ['title'],
                                         blank_fields=[],
                                         required_fields=['title'])
        fields = ['id'] + BlogCategory().get_all_fields()


class BlogBannerSerializer(DynamicSerializer):
    remove_field_view = {
        'list': [],
        'create': [],
        'update': [],
    }

    class Meta:
        model = BlogBanner
        extra_kwargs = api_error_creator(model,
                                         model.get_serializer_fields(),
                                         blank_fields=[],
                                         required_fields=[])
        fields = ['id', ] + model.get_serializer_fields()


class BlogPartnerSerializer(DynamicSerializer):
    remove_field_view = {
        'list': [],
        'create': [],
        'update': [],
    }

    class Meta:
        model = BlogPartner
        extra_kwargs = api_error_creator(model,
                                         model.get_serializer_fields(),
                                         blank_fields=[],
                                         required_fields=[])
        fields = ['id', ] + model.get_serializer_fields()
