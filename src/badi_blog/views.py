from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.text import slugify
from django.views.generic import ListView, DetailView

from badi_blog.models import *

from django.conf import settings

CONFIG_JSON = getattr(settings, "CONFIG_JSON", {})


class BlogDetailView(DetailView):
    template_name = "blog/blog-detail.html"
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_videos'] = context['object'].categories.first().news.exclude(id=context['object'].id)[:4]
        context['object_comments_count'] = context['object'].comments.filter(is_accepted=True).count()
        context['seo_title'] = self.object.title + ' | ' + CONFIG_JSON.get('site_title')
        if self.object.short:
            context['seo_desc'] = self.object.short
        if self.object.tags.first():
            context['seo_tags'] = ','.join([tag.title for tag in self.object.tags.all()])
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.visited()
        return obj


class BlogView(ListView):
    extra_context = {
        'title': 'وبلاگ',
        'seo_title': 'وبلاگ | ' + CONFIG_JSON.get('site_title'),
        'categories': BlogCategory.objects.all().select_related('father')
    }
    paginate_by = 12
    template_name = "blog.html"
    queryset = BlogPost.objects.select_related('writer').prefetch_related('comments')
    page_kwarg = 'page'

    def get_queryset(self):
        qs = self.queryset
        category_pk = self.kwargs.get('category_pk')
        if category_pk:
            qs = qs.filter(categories=category_pk)
        tag_pk = self.kwargs.get('tag_pk')
        if tag_pk:
            qs = qs.filter(tags=tag_pk)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['category_pk'] = self.kwargs.get('category_pk')
        context['tag_pk'] = self.kwargs.get('tag_pk')
        if context['category_pk']:
            cate = get_object_or_404(BlogCategory, pk=context['category_pk'])
            context['url_page'] = '/blog/category/' + str(cate.id) + '/' + slugify(cate.title, True) + '/page/'
        elif context['tag_pk']:
            tag = get_object_or_404(BlogTag, pk=context['tag_pk'])
            context['url_page'] = '/blog/tag/' + str(tag.id) + '/' + slugify(tag.title, True) + '/page/'
        else:
            context['url_page'] = '/blog/page/'
        if self.request.GET.get('page'):
            context['seo_title'] = 'وبلاگ | صفحه ' + self.request.GET.get('page') + ' | ' + CONFIG_JSON.get(
                'site_title')
        return context
