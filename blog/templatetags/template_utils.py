from django import template

register = template.Library()

@register.filter
def convert_phone_format(s):
    num = s.strip()
    size = len(num)
    if len(num) == 0:
        return num
    return '{0}-{1}-{2}'.format(num[0:size-7], num[size-7:size-4], num[size-5:-1])