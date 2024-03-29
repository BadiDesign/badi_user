import datetime

from django import template
from django.conf import settings
from django.utils.text import slugify

from badi_ticket.models import Ticket
from badi_utils.date_calc import custom_change_date, gregorian_to_jalali
from random import shuffle

register = template.Library()
CONFIG_JSON = getattr(settings, "CONFIG_JSON", {})


@register.simple_tag(takes_context=True)
def get_query_string(context):
    params = context.request.META.get('QUERY_STRING')
    if params:
        params = '?' + params
    return params


@register.filter(name='get_absolute_url')
def get_absolute_url(obj):
    return obj.get_absolute_url()


@register.filter()
def minus(obj, value):
    return obj - value


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
def is_filled_profile(context):
    return context.request.user.is_filled_profile()


@register.simple_tag()
def get_text(index):
    return CONFIG_JSON.get(index) if CONFIG_JSON.get(index) else '---'


@register.simple_tag(takes_context=True)
def last_activities(context):
    user = context.request.user
    if user.is_authenticated:
        return user.logs.all()[:10]
    return []


@register.filter()
def get_log_icon(log):
    if log.title == "Custom":
        return "fa-info"
    if log.title == "Login":
        return "fa-arrow-down"
    if log.title == "LogOut":
        return "fa-arrow-up"
    if log.title == "Insert":
        return "fa-plus"
    if log.title == "Edit":
        return "fa-pen"
    if log.title == "Remove":
        return "fa-trash"
    return 'fa-info'


@register.filter()
def get_log_color(log):
    if log.title == "Custom":
        return "info"
    if log.title == "Login":
        return "success"
    if log.title == "LogOut":
        return "info"
    if log.title == "Insert":
        return "primary"
    if log.title == "Edit":
        return "warning"
    if log.title == "Remove":
        return "danger"
    return 'fa-info'
