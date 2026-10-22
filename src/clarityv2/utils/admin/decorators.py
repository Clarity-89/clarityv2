from functools import wraps

from django.urls import reverse
from django.utils.html import format_html_join


def get_urlname(obj):
    app_label, model_name = obj._meta.app_label, obj._meta.model_name
    return 'admin:{}_{}_change'.format(app_label, model_name)


def link_list(urlname=None, short_description=None):
    """
    Decorates a modeladmin method that returns a queryset of related objects to
    render them as a comma-separated list of admin change links.
    """
    def decorator(method):
        if short_description:
            method.short_description = short_description

        @wraps(method)
        def f(*args, **kwargs):
            related_qs = method(*args, **kwargs)
            return format_html_join(
                ', ', '<a href="{}">{}</a>',
                ((reverse(urlname or get_urlname(rel), args=[rel.pk]), rel) for rel in related_qs),
            )
        return f
    return decorator
