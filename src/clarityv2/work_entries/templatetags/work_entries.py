from decimal import Decimal

from django import template

from clarityv2.invoices.constants import TWO_DIGITS

register = template.Library()


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds / 3600

    return '{}'.format(hours)


@register.simple_tag
def total_price(project, total_hours):
    if project.flat_fee:
        return project.flat_fee
    rate = project.base_rate

    return (Decimal(total_hours) * rate).quantize(TWO_DIGITS)
