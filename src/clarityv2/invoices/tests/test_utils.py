from datetime import date

from django.test import RequestFactory, TestCase, override_settings

from freezegun import freeze_time
from privates.test import temp_private_root

from clarityv2.accounts.models import AdminUser
from clarityv2.crm.tests.factories import ProjectFactory

from ..utils import (
    generate_ref_number, generate_rf_reference, render_invoice_pdf
)
from .factories import InvoiceFactory, InvoiceItemFactory


@temp_private_root()
class InvoiceUtilsTests(TestCase):
    @freeze_time('2015-10-21')
    # UrlFetcher only falls back to staticfiles finders (no collectstatic in tests) when DEBUG is on
    @override_settings(DEBUG=True)
    def test_render_pdf(self):
        AdminUser.get_solo()  # the invoice tags read the singleton with .objects.get()
        project = ProjectFactory.create(flat_fee=3500)
        invoice = InvoiceFactory.create(client=project.client, date=date(2015, 10, 15))
        InvoiceItemFactory.create(invoice=invoice, project=project, rate=3500, amount=1, source_object=project)
        invoice.generate()

        render_invoice_pdf(RequestFactory().get('/'), invoice)

        self.assertEqual(invoice.pdf.name, 'invoices/2015/10/201500001.pdf')
        with invoice.pdf.open('rb') as pdf:
            self.assertEqual(pdf.read(5), b'%PDF-')


class InvoiceReferenceTests(TestCase):
    def test_generate_ref_number(self):
        # Should work for generic numbers
        self.assertEqual('1234561', generate_ref_number(123456))
        self.assertEqual('7778282823', generate_ref_number(777828282))
        self.assertEqual('2019000280', generate_ref_number(201900028))

        # Should handle leading 0
        self.assertEqual('1234561', generate_ref_number('0123456'))
        self.assertEqual('1234561', generate_ref_number('0000123456'))
        self.assertEqual('7778282823', generate_ref_number('0777828282'))
        self.assertEqual('2019000280', generate_ref_number('0201900028'))

    def test_generate_rf_reference(self):
        # Should work for generic numbers
        self.assertEqual('RF341234561', generate_rf_reference(123456))
        self.assertEqual('RF817778282823', generate_rf_reference(777828282))
        self.assertEqual('RF372019000280', generate_rf_reference(201900028))

        # Should handle leading 0
        self.assertEqual('RF341234561', generate_rf_reference('0123456'))
        self.assertEqual('RF341234561', generate_rf_reference('0000123456'))
        self.assertEqual('RF817778282823', generate_rf_reference('0777828282'))
        self.assertEqual('RF372019000280', generate_rf_reference('0201900028'))
