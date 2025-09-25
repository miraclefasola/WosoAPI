# core/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def div(value, arg):
    if arg and value:
        return value / arg
    return 0


@register.filter
def dict_get(d, key):
    return d.get(key)
