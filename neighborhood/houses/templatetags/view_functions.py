from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()


def prettify_none(optional):
    return optional if optional else '-- '


def maybe_intcomma(num):
    if num:
        return intcomma(num)
    return

register.filter('maybe_intcomma', maybe_intcomma)
register.filter('prettify_none', prettify_none)
