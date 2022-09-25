import datetime

from django import template
from django.utils.text import slugify

from advertisement.models import Page, PostCategory
from blog.models import BlogNews
from plugins.dynamic_models import gregorian_to_jalali
from plugins.project_config import CONFIG_JSON
from plugins.utils import custom_change_date
from setting.models import CategoryNews
from ticket.models import Ticket
from random import shuffle

register = template.Library()


@register.filter(name='date_jalali')
def date_jalali(value, mode=1):
    if value != None:
        if mode == 1:
            date_time = value

            if date_time.minute < 10:
                minute = '0' + str(date_time.minute)
            else:
                minute = str(date_time.minute)
            if date_time.second < 10:
                second = '0' + str(date_time.second)
            else:
                second = str(date_time.second)

            if date_time.hour < 10:
                hour = '0' + str(date_time.hour)
            else:
                hour = str(date_time.hour)
            shamsi = gregorian_to_jalali(date_time.year, date_time.month, date_time.day)
            return " {h}:{m}:{s} {year}/{month}/{day}".format(year=shamsi[0],
                                                              month=shamsi[1],
                                                              day=shamsi[2],
                                                              h=date_time.hour,
                                                              m=minute,
                                                              s=second)
        elif mode == 2:
            d = value.strftime('%Y-%m-%d')
            year, month, day = d.split('-')
            shamsi = gregorian_to_jalali(int(year), int(month), int(day))
            return "{year}/{month}/{day}".format(year=shamsi[0], month=shamsi[1], day=shamsi[2])
    else:
        return "بدون ثبت"


@register.filter(name='empty')
def empty(value, default="بدون ثبت"):
    try:
        if value != None:
            return value
        else:
            return default
    except:
        return default


@register.filter(name='append')
def append(value, val):
    return str(value) + str(val)


@register.filter(name='is_active')
def is_active(value):
    return value.is_active()


@register.filter(name='reverse')
def reverse(value):
    return value.reverse()


@register.filter(name='get_picture')
def get_picture(new):
    return new.picture.url if new.picture else ''


@register.filter(name='get_url')
def get_url(new):
    return 'news/{0}/{1}'.format(new.id, new.title)


@register.filter(name='get_writer_url')
def get_writer_url(new):
    return f'author/{new.writer.id}/{new.writer.get_full_name()}'


@register.filter(name='get_slider_picture')
def get_slider_picture(new):
    if new.slider_picture:
        return new.slider_picture.url
    return new.picture.url if new.picture else ''


@register.filter(name='get_full_name')
def get_full_name(user):
    return user.get_full_name()


@register.simple_tag(takes_context=True)
def user_fullname(context):
    user = context.request.user
    if user.is_authenticated:
        return user.get_full_name()
    return ''


@register.simple_tag()
def car_categories():
    cars = PostCategory.objects.filter(title="ماشین").first()
    return cars.children.all()


@register.simple_tag()
def week_day():
    week_days = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "يکشنبه", ]
    weekday = datetime.datetime.today().weekday()
    return week_days[weekday]


@register.simple_tag()
def today_date():
    today = datetime.date.today()
    return custom_change_date(today, 2)


@register.simple_tag()
def today_date_str():
    today = datetime.datetime.now()
    return custom_change_date(today, 7)


@register.simple_tag(takes_context=True)
def my_info(context):
    user = context.request.user
    if not user.is_authenticated:
        return {}
    return {
        'unread_messages': Ticket.unread_messages_of(user),
        'amount': user.amount,
        'posts': user.posts.count(),
        'freeposters': user.freeposters.count(),
    }


@register.simple_tag(takes_context=True)
def get_query_string(context):
    params = context.request.META.get('QUERY_STRING')
    if params:
        params = '?' + params
    return params


@register.filter(name='slugify_utf8')
def slugify_utf8(value):
    return slugify(value, True)


@register.simple_tag(takes_context=True)
def last_12_pages(context):
    pages = list(Page.objects.all())
    shuffle(pages)
    return pages[:12]


@register.simple_tag(takes_context=True)
def last_breaking_news(context):
    news = BlogNews.objects.filter(breaking_title__isnull=False)[:10]
    return news


@register.simple_tag(takes_context=True)
def suggest_news(context):
    news = BlogNews.objects.filter(is_recommend=True)[:4]
    return news


@register.simple_tag(takes_context=True)
def categories(context):
    cats = CategoryNews.objects.filter(index_show=True)
    return cats


@register.simple_tag(takes_context=True)
def slider_news(context, count=7):
    news = BlogNews.objects.filter(slider_title__isnull=False)[:count]
    return news


@register.simple_tag(takes_context=True)
def week_top_news(context):
    week_ago = datetime.datetime.now() - datetime.timedelta(days=8)
    news = BlogNews.objects.filter(created_at__gt=week_ago).order_by('view')[:5]
    return news


@register.simple_tag(takes_context=True)
def last_news(context, count=15):
    news = BlogNews.objects.all()[:count]
    return news


@register.simple_tag(takes_context=True)
def is_filled_profile(context):
    return context.request.user.is_filled_profile()


@register.simple_tag()
def get_text(index):
    return CONFIG_JSON.get(index) if CONFIG_JSON.get(index) else '---'
