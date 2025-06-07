from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from badi_utils.dynamic_api import api_error_creator, DynamicSerializer, CustomValidation
from badi_blog.models import *
from badi_utils.validations import PersianValidations


class BlogPostSerializer(DynamicSerializer):
    remove_field_view = {
        'create': ['writer', 'tags'],
        'update': ['writer', 'tags'],
    }

    class Meta:
        model = BlogPost
        extra_kwargs = api_error_creator(BlogPost, BlogPost().get_all_fields(),
                                         blank_fields=[],
                                         required_fields=[])
        # depth = 1
        fields = ['id'] + BlogPost().get_all_fields()

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
        extra_kwargs = api_error_creator(BlogCategory, BlogCategory().get_all_fields(),
                                         blank_fields=[],
                                         required_fields=['title'])
        fields = ['id'] + BlogCategory().get_all_fields()


class BlogQuestionAnswerSerializer(DynamicSerializer):
    class Meta:
        model = BlogQuestionAnswer
        extra_kwargs = api_error_creator(model, model().get_all_fields(),
                                         blank_fields=[],
                                         required_fields=[])
        fields = ['id'] + model().get_all_fields()


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


class BlogImageSerializer(DynamicSerializer):
    remove_field_view = {
        'create': [],
        'update': [],
    }

    class Meta:
        model = BlogImage
        extra_kwargs = api_error_creator(model, model().get_all_fields(),
                                         blank_fields=[],
                                         required_fields=[])
        fields = model().get_all_fields()

    def create(self, validated_data):
        res = super().create(validated_data)
        return res
