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
def add_attrs(field, args):
    attrs = {}
    for a in args.split(','):
        k, v = a.split(':')
        attrs[k] = v
    return field.as_widget(attrs=attrs)


@register.filter
def get_field_type(field):
    if hasattr(field.field.widget, 'input_type'):
        return field.field.__class__.__name__ + '_' + field.field.widget.input_type
    return field.field.__class__.__name__
    

@register.filter
def join(l, opr):
    if isinstance(l, list):
        if opr == 'email':
            emails = []
            for a in l:
                emails.append(f'<a href="mailto={a}">{a}</a>')
            return '<br /> '.join(emails)
        return f'{opr} '.join(l)
    return l



# Helper functions

@register.filter
def inspect(data):
    return None
