from django import template
from django.conf import settings

from clarityv2.accounts.models import AdminUser


register = template.Library()


@register.inclusion_tag('invoices/tags/address.html')
def company_details(client=None):
    if client is not None:
        return {
            'client': client,
            'company_name': client.name,
            'company_address': [client.address, client.postal_code + ' ' + client.city, client.get_country_display()],
            'company_tax_identifier': client.vat_number,
        }
    else:
        client = AdminUser.objects.get()
        return {
            'client': client,
            'company_name': client.get_entity_name,
            'company_address': [client.get_full_street_address(), client.postal_code + ' ' + client.city,
                                client.get_country_display()],
            'company_tax_identifier': client.vat_number
        }


@register.simple_tag
def company_field(prop):
    key = 'INVOICES_COMPANY_%s' % prop
    return getattr(settings, key)


@register.inclusion_tag('invoices/tags/identity_string.html')
def identity_string():
    user = AdminUser.objects.get()
    return {
        'phone': user.phone,
        'email': user.email,
        'business_id': user.business_id
    }


@register.simple_tag
def iban():
    user = AdminUser.objects.get()
    return user.iban


@register.inclusion_tag('invoices/tags/bank_details.html')
def bank_details():
    user = AdminUser.objects.get()
    return {
        'bank': user.bank,
        'branch': user.bank_branch,
        'iban': user.iban,
        'swift': user.swift
    }
