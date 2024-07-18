from django import template

register = template.Library()


@register.simple_tag()
def test():
    return "Badi Utils template tags works"


@register.filter(name='get_cover')
def get_cover(new, default=""):
    return new.picture.url if new.picture else default


@register.filter(name='remove_page')
def remove_page(value):
    def check(x):
        return 'page' not in x

    if value:
        value = value.split('?')[1]
        value = value.split('&')
        value = list(filter(check, value))
    return '&'.join(value)
