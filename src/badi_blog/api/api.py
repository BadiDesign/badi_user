from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from badi_utils.dynamic_api import DynamicModelApi, DynamicModelReadOnlyApi
from badi_blog.api.serializers import *
from badi_blog.filter import *
from badi_blog.models import *


class BlogPostViewSet(DynamicModelApi):
    columns = ['id', 'picture', 'title', 'categories', 'writer', 'slider_title', 'is_recommend', 'view', 'created_at']
    order_columns = ['id', 'picture', 'title', 'categories', 'writer', 'slider_title', 'is_recommend', 'view',
                     'created_at']
    model = BlogPost
    queryset = BlogPost.objects.select_related('writer').prefetch_related('comments')
    serializer_class = BlogPostSerializer
    filterset_class = BlogPostFilter
    custom_perms = {
        'self': True
    }

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, qs):
        if self.action == 'datatable':
            return BlogPostFilter(self.request.POST).qs.select_related('writer').prefetch_related('comments')
        if self.action in ['list', 'retrieve']:
            return BlogPostFilter(self.request.POST).qs.select_related('writer').prefetch_related('comments')
        return super().filter_queryset(qs)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 10


class BlogCommentViewSet(DynamicModelApi):
    model = BlogComment
    serializer_class = BlogCommentSerializer
    filterset_class = BlogCommentFilter
    queryset = BlogComment.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
    custom_perms = {
        'create': False,
        'list': False,
    }
    switches = {
        'is_accepted': {
            'true': '/api/v1/blogcomment/change_state_accepted/0',
            'false': '/api/v1/blogcomment/change_state_accepted/0',
        },
        'is_rejected': {
            'true': '/api/v1/blogcomment/change_state_rejected/0',
            'false': '/api/v1/blogcomment/change_state_rejected/0',
        },
    }

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        if self.action in ['list', ]:
            qs = BlogCommentFilter(self.request._request.GET).qs.filter(is_accepted=True, replay=None)
        if self.action == 'datatable':
            qs = BlogCommentFilter(self.request.data).qs
        return qs

    @action(methods=['put'], detail=False, url_path='change_state_accepted/(?P<pk>[^/.]+)')
    def change_state_accepted(self, request, pk, *args, **kwargs):
        animal = self.model.objects.get(pk=pk)
        animal.is_accepted = not animal.is_accepted
        animal.save()
        return JsonResponse(
            {'message': 'وضیعت تغییر کرد به: {0}'.format('تایید شده' if animal.is_accepted else 'تایید نشده')})

    @action(methods=['put'], detail=False, url_path='change_state_rejected/(?P<pk>[^/.]+)')
    def change_state_rejected(self, request, pk, *args, **kwargs):
        animal = self.model.objects.get(pk=pk)
        animal.is_rejected = not animal.is_rejected
        animal.save()
        return JsonResponse(
            {'message': 'وضیعت تغییر کرد به: {0}'.format('رد شده' if animal.is_rejected else 'رد نشده')})


class BlogCategoryViewSet(DynamicModelApi):
    model = BlogCategory
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    columns = model().get_datatable_columns()
    custom_perms = {
        'list': False
    }


class BlogBannerViewSet(DynamicModelApi):
    model = BlogBanner
    queryset = BlogBanner.objects.all()
    serializer_class = BlogBannerSerializer
    custom_perms = {
        'list': False
    }


class BlogQuestionAnswerViewSet(DynamicModelApi):
    model = BlogQuestionAnswer
    queryset = BlogQuestionAnswer.objects.all()
    serializer_class = BlogQuestionAnswerSerializer
    custom_perms = {
        'list': False
    }


class BlogPartnerViewSet(DynamicModelApi):
    model = BlogPartner
    queryset = BlogPartner.objects.all()
    columns = BlogPartner.get_datatable_fields()
    serializer_class = BlogPartnerSerializer
    filterset_class = BlogPartnerFilter
    custom_perms = {
        'create': 'blog.can_blog_partner',
        'update': 'blog.can_blog_partner',
        'destroy': 'blog.can_blog_partner',
        'datatable': 'blog.can_blog_partner',
        'list': False,
    }


class BlogImageViewSet(DynamicModelApi):
    model = BlogImage
    queryset = BlogImage.objects.all()
    serializer_class = BlogImageSerializer
    pagination_class = CustomPagination
    custom_perms = {
    }
    columns = model().get_all_fields()
    filterset_class = BlogImageFilter

    def filter_queryset(self, qs):
        if self.action == 'list':
            return BlogImageFilter(self.request.query_params).qs
        return super().filter_queryset(qs)
