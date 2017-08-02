from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def json_safe(value):
    return mark_safe(value.replace("<", "\\u003c").replace(">", "\\u003e"))
