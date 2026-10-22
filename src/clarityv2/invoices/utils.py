"""
Utility functions for invoices.
"""
from io import BytesIO

from django.db.models import Count
from django.utils import translation

from clarityv2.utils.pdf import render_to_pdf


def get_invoice_context(invoice, **extra):
    tax_rates = invoice.invoiceitem_set.values("tax_rate").annotate(
        num=Count("tax_rate")
    )
    context = {
        "invoice": invoice,
        "tax_rates": tax_rates,
        "items": invoice.invoiceitem_set.select_related("project").order_by(
            "project", "tax_rate"
        ),
        **extra,
    }
    return context


def render_invoice_pdf(request, invoice, template_name="invoices/invoice_detail.html"):
    # render the invoice in the client's language
    lang_code = invoice.client.language
    translation.activate(lang_code)

    context = get_invoice_context(invoice, request=request)
    pdf = render_to_pdf(template_name, context)[1]
    filename = "{}.pdf".format(invoice.invoice_number)
    invoice.pdf.save(filename, BytesIO(pdf))

    # go back to the previous language
    if hasattr(request, "LANGUAGE_CODE"):
        translation.activate(request.LANGUAGE_CODE)
    else:
        translation.deactivate()


INVOICE_MULTIPLIERS = [1, 3, 7]
RF_NUM_BASE = '2715'


def generate_ref_number(base):
    """
    Generate Finnish reference number, where it must be between 4 (3 base chars + checksum) and
    20 (19 base + 1 checksum) characters long.
    Rules for generating the checksum: https://www.finanssiala.fi/maksujenvalitys/dokumentit/Forming_a_Finnish_reference_number.pdf
    """
    str_number = str(base).lstrip("0")

    if 19 < len(str_number) < 3:
        raise ValueError('Invoice number must be min 3 and max 19 chars long')

    checksum = 0
    for i in range(len(str_number)):
        checksum += INVOICE_MULTIPLIERS[i % len(INVOICE_MULTIPLIERS)] * int(str_number[i])

    checksum_num = 10 - checksum % 10
    if checksum_num == 10:
        checksum_num = 0

    return f'{str_number}{checksum_num}'


def get_rf_checksum(rf_base):
    """
    Get the two checksum digits by subtracting modulo 97 of RF base from 98
    """

    remainder = int(rf_base) % 97
    digits = 98 - remainder

    if digits < 10:
        return '0' + str(digits)

    return str(digits)


def generate_rf_reference(base):
    """
    Generate Creditor reference: https://en.wikipedia.org/wiki/Creditor_Reference for international payments
    Format: FR + 2 checksum numbers + Finnish reference number
    """
    ref_number = generate_ref_number(base)
    rf_base = ref_number + RF_NUM_BASE + '00'

    return 'RF' + get_rf_checksum(rf_base) + ref_number


def generate_invoice_reference(client, invoice_number):
    if client.country == 'FI':
        return generate_ref_number(invoice_number)
    return generate_rf_reference(invoice_number)
