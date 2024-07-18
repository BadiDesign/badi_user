from django.db.models import Q
from django_filters import rest_framework as filters
from badi_blog.models import *
from badi_user.filter import TextIn


class BlogPostFilter(filters.FilterSet):
    class Meta:
        model = BlogPost
        fields = [
            'writer',
            'categories',
            'is_recommend',
        ]

    title = TextIn(field_name='title')
    breaking_title = TextIn(field_name='breaking_title')
    slider_title = TextIn(field_name='slider_title')
    source_title = TextIn(field_name='source_title')
    source_link = TextIn(field_name='source_link')


class BlogCommentFilter(filters.FilterSet):
    class Meta:
        model = BlogComment
        fields = [
            'post',
            'is_accepted',
            'is_rejected',
        ]


class BlogBannerFilter(filters.FilterSet):
    class Meta:
        model = BlogBanner
        fields = [
            'lang',
        ]


class BlogPartnerFilter(filters.FilterSet):
    class Meta:
        model = BlogPartner
        fields = [
        ]

    name = TextIn(field_name='name')


class BlogImageTextIn(TextIn):

    def filter(self, qs, value):
        if value:
            qs = qs.filter(Q(alt__icontains=value) | Q(url__icontains=value) | Q(image__icontains=value))
        return qs


class BlogImageFilter(filters.FilterSet):
    class Meta:
        model = BlogImage
        fields = [
        ]

    alt = BlogImageTextIn(field_name='alt')
