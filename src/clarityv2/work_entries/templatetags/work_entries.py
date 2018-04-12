from decimal import Decimal

from django import template

from clarityv2.invoices.constants import TWO_DIGITS

register = template.Library()


@register.filter
def duration(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds / 3600

    return '{}'.format(round(float(hours), 2))


@register.simple_tag
def total_price(project, total_hours):
    if project.flat_fee:
        return project.flat_fee
    rate = project.base_rate

    return (Decimal(total_hours) * rate).quantize(TWO_DIGITS)


def total_hours(entries):
    total = 0.0
    for entry in entries:
        total = total + (entry.duration.total_seconds() / 3600)
    return round(float(total), 2)


@register.simple_tag
def hours_per_month(entries):
    return total_hours(entries)


@register.simple_tag
def total_per_month(entries, project):
    if project.flat_fee:
        return project.flat_fee

    rate = project.base_rate
    total = total_hours(entries)

    return (Decimal(round(float(total), 2)) * rate).quantize(TWO_DIGITS)
