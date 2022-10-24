from django import template

register = template.Library()


@register.simple_tag()
def test():
    return "Badi Utils template tags works"
