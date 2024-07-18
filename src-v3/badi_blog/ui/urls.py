from badi_blog.models import BlogPost, BlogComment
from badi_utils.dynamic import *
from badi_blog.ui.views import *

category_urls = multi_generator_url(BlogCategory(), create=BlogCategoryCreateView, update=BlogCategoryUpdateView)
banner_urls = multi_generator_url(BlogBanner(), create=BlogBannerCreateView, update=BlogBannerUpdateView)
partner_urls = multi_generator_url(BlogPartner(), create=BlogPartnerCreateView, update=BlogPartnerUpdateView)
urlpatterns = [
                  generate_url(BlogPost(), create=BlogPostCreateView),
                  generate_url(BlogPost(), view=BlogPostListView),
                  generate_url(BlogImage(), view=BlogImageListView),
                  generate_url(BlogPost(), update=BlogPostUpdateView),
                  generate_url(BlogComment(), list=BlogCommentList),
                  generate_url(BlogBanner(), list=BlogBannerListView),
              ] + category_urls + banner_urls + partner_urls
