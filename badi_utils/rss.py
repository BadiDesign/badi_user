from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import DefaultFeed
from django.conf import settings

CONFIG_JSON = getattr(settings, "CONFIG_JSON", {})
site = Site.objects.filter(id=getattr(settings, "SITE_ID", None)).first() or 'BadiDesign.ir'
SITE_URL = 'https://' + site.domain


class CorrectMimeTypeFeed(DefaultFeed):
    content_type = 'application/xml; charset=utf-8'


class DynamicFeed(Feed):
    title = CONFIG_JSON['title']
    description = CONFIG_JSON['description']
    feed_type = CorrectMimeTypeFeed

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
