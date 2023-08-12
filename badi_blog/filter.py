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
