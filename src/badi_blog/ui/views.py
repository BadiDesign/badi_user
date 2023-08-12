from badi_utils.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from badi_blog.filter import *
from badi_blog.models import *


class BlogPostListView(DynamicListView):
    model = BlogPost
    datatable_cols = ['#', 'تصویر', 'عنوان', 'دسته بندی ها', 'نویسنده', 'اسلایدر', 'پیشنهادی', 'بازدید', 'زمان ثبت']

    def get_extra_context(self, context):
        context['filters'] = BlogPostFilter(self.request.POST)
        return super().get_extra_context(context)


class BlogPostCreateView(DynamicCreateView):
    model = BlogPost
    datatableEnable = False

    def get_extra_context(self, context):
        context['back'] = '/dashboard/blogpost/list'
        return context


class BlogPostUpdateView(DynamicUpdateView):
    model = BlogPost
    success_url = '/dashboard/blogpost/list'


class BlogCommentList(DynamicListView):
    model = BlogComment
    datatable_cols = model.get_datatable_verbose()
    extra_context = {
        'filters': BlogCommentFilter()
    }


class BlogCategoryCreateView(DynamicCreateView):
    model = BlogCategory


class BlogCategoryUpdateView(DynamicUpdateView):
    model = BlogCategory


class BlogBannerListView(DynamicListView):
    model = BlogBanner
    datatable_cols = BlogBanner().get_datatable_verbose_names()
    permission_required = 'blog.can_manage_banner'

    def get_extra_context(self, context):
        context['filters'] = BlogBannerFilter(self.request.POST)
        return super().get_extra_context(context)


class BlogBannerCreateView(DynamicCreateView):
    model = BlogBanner
    datatableEnable = False
    permission_required = 'blog.can_manage_banner'

    def get_extra_context(self, context):
        context['back'] = 'list'
        return context


class BlogBannerUpdateView(DynamicUpdateView):
    model = BlogBanner
    permission_required = 'blog.can_manage_banner'
    success_url = '../list'


class BlogPartnerCreateView(DynamicCreateView):
    model = BlogPartner
    extra_context = {
        'filters': BlogPartnerFilter
    }
    permission_required = 'blog.can_blog_partner'


class BlogPartnerUpdateView(DynamicUpdateView):
    model = BlogPartner
    success_url = '../create'
    permission_required = 'blog.can_blog_partner'
