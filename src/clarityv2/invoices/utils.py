"""
Utility functions for invoices.
"""
from io import BytesIO

from django.core.files import File
from django.db.models import Count
from django.template import loader
from django.utils import translation

import weasyprint
from sendfile import sendfile

from clarityv2.utils.pdf import UrlFetcher
from clarityv2.utils.views.pdf import (
    PDFTemplateResponse, PDFTemplateResponseMixin
)


def render_invoice_pdf(request, invoice, template_name='invoices/invoice_detail.html'):
    # render the invoice in the client's language
    lang_code = invoice.client.language
    translation.activate(lang_code)

    if isinstance(template_name, (list, tuple)):
        template = loader.select_template(template_name)
    else:
        template = loader.get_template(template_name)

    tax_rates = invoice.invoiceitem_set.values('tax_rate').annotate(num=Count('tax_rate'))
    context = {
        'invoice': invoice,
        'tax_rates': tax_rates,
        'items': invoice.invoiceitem_set.select_related('project').order_by('project', 'tax_rate'),
        'request': request,
    }
    html = template.render(context)
    base_url = request.build_absolute_uri("/")
    url_fetcher = UrlFetcher(request, base_url)
    wp = weasyprint.HTML(string=html, base_url=base_url, url_fetcher=url_fetcher)
    # pdf as bytes
    buffer = BytesIO()
    wp.write_pdf(target=buffer)
    filename = '{}.pdf'.format(invoice.invoice_number)
    invoice.pdf.save(filename, File(buffer))

    # go back to the previous language
    if hasattr(request, 'LANGUAGE_CODE'):
        translation.activate(request.LANGUAGE_CODE)
    else:
        translation.deactivate()


class InvoicePDFTemplateResponse(PDFTemplateResponse):

    def __init__(self, invoice=None, *args, **kwargs):
        self.invoice = invoice
        super(InvoicePDFTemplateResponse, self).__init__(*args, **kwargs)

    @property
    def rendered_content(self):
        """
        Read the invoices pdf, or generate it and return the rendered pdf.
        """
        assert self.invoice is not None

        if not self.invoice.pdf:
            render_invoice_pdf(self._request, self.invoice, template_name=self.template_name)
        return self.invoice.pdf.read()


class InvoicePDFTemplateResponseMixin(PDFTemplateResponseMixin):
    response_class = InvoicePDFTemplateResponse

    def render_to_response(self, *args, **kwargs):
        # if the pdf exists, use sendfile
        if self.object.pdf:
            return sendfile(
                self.request, self.object.pdf.path,
                attachment=True, attachment_filename=self.get_filename()
            )
        kwargs['invoice'] = self.object
        return super(InvoicePDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


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
