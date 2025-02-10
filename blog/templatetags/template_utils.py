from django import template
from django.utils.text import slugify

register = template.Library()


@register.filter
def convert_phone_format(s):
    num = s.strip()
    size = len(num)
    if len(num) == 0:
        return num
    return '{0}-{1}-{2}'.format(num[0:size-7], num[size-7:size-4], num[size-5:-1])


@register.filter
def minus(a, b):
    return a - b


@register.filter
def slug(s):
    return slugify(s)


# Helper functions

@register.filter
def inspect(data):
    return None
