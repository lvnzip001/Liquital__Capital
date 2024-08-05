from django import template
from django.utils.safestring import SafeString


register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def multiply_by_100(value):
    try:
        return float(value) * 100
    except (ValueError, TypeError):
        return value