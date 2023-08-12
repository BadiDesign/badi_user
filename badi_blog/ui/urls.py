from badi_blog.models import BlogPost, BlogComment
from badi_utils.dynamic import *
from badi_blog.ui.views import *

category_urls = multi_generator_url(BlogCategory(), create=BlogCategoryCreateView, update=BlogCategoryUpdateView)
urlpatterns = [
                  generate_url(BlogPost(), create=BlogPostCreateView),
                  generate_url(BlogPost(), view=BlogPostListView),
                  generate_url(BlogPost(), update=BlogPostUpdateView),
                  generate_url(BlogComment(), list=BlogCommentList),
              ] + category_urls
