import datetime
from django import template
from django.conf import settings
from django.utils.text import slugify
from random import shuffle

register = template.Library()
CONFIG_JSON = getattr(settings, "CONFIG_JSON", {})


@register.filter(name='get_cover')
def get_cover(new, default=""):
    return new.picture.url if new.picture else default


@register.filter(name='get_film')
def get_film(new, default=""):
    return ('/stream?url=' + new.film.url) if new.film else new.link or default


@register.filter(name='get_film_link')
def get_film_link(new, default=""):
    return new.film.url if new.film else new.link or default
