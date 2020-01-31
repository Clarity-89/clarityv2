import os
from datetime import date

from django.test import RequestFactory, TestCase

from freezegun import freeze_time

from clarityv2.crm.tests.factories import ProjectFactory

from ..utils import render_invoice_pdf, generate_ref_number
from .factories import InvoiceFactory, InvoiceItemFactory


class InvoiceUtilsTests(TestCase):
    pass
    # @freeze_time('2015-10-21')
    # def test_render_pdf(self):
    #     project = ProjectFactory.create(flat_fee=3500)
    #     invoice = InvoiceFactory.create(client=project.client, date=date(2015, 10, 15))
    #     InvoiceItemFactory.create(
    #         invoice=invoice, project=project,
    #         rate=3500, amount=1,
    #         source_object=project
    #     )
    #
    #     self.assertFalse(invoice.invoice_number)
    #     invoice.generate()
    #
    #     request = RequestFactory().get('/')
    #     render_invoice_pdf(request, invoice)
    #
    #     self.assertEqual(invoice.pdf.name, 'invoices/2015/10/201500001.pdf')
    #     self.assertTrue(os.path.exists(invoice.pdf.path))


class InvoiceReferenceTests(TestCase):
    def test_generate_ref_number(self):
        # Should work for generic numbers
        self.assertEquals('1234561', generate_ref_number(123456))
        self.assertEquals('7778282823', generate_ref_number(777828282))
        self.assertEquals('2019000280', generate_ref_number(201900028))

        # Should handle leading 0
        self.assertEquals('1234561', generate_ref_number('0123456'))
        self.assertEquals('1234561', generate_ref_number('0000123456'))
        self.assertEquals('7778282823', generate_ref_number('0777828282'))
        self.assertEquals('2019000280', generate_ref_number('0201900028'))
