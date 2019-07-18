import readtime

from django import template

register = template.Library()


@register.simple_tag
def time_to_read(text):
    result = readtime.of_text(text)

    return f"{result.text} read"
