from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase, override_settings
from django.utils import timezone

from freezegun import freeze_time

from clarityv2.crm.models import TaxRates
from clarityv2.crm.tests.factories import ClientFactory, ProjectFactory
from clarityv2.work_entries.tests.factories import WorkEntryFactory

from ..models import InvoiceItem, InvoiceItemTemplate
from .factories import InvoiceFactory, InvoiceItemFactory


class InvoiceTests(TestCase):

    @freeze_time('2015-10-02')
    def test_pickup_work_entries(self):
        """
        Test that the work entries are correctly picked up for a given invoice date.
        """
        client1, client2 = ClientFactory.create_batch(2)
        project1, project2 = ProjectFactory.create_batch(2, client=client1, vat=TaxRates.standard)
        project3 = ProjectFactory.create(client=client2)

        # worked a bit on project 1
        WorkEntryFactory.create(project=project1, date=date(2015, 9, 14), duration=timedelta(hours=4))

        # worked a bit on project 2
        WorkEntryFactory.create(project=project2, date=date(2015, 9, 14), duration=timedelta(hours=2, minutes=30))
        WorkEntryFactory.create(project=project2, date=date(2015, 9, 30), duration=timedelta(hours=2, minutes=30))

        # future entry to be ignored
        WorkEntryFactory.create(project=project1, date=date(2015, 10, 1), duration=timedelta(hours=3))

        # different client
        WorkEntryFactory.create(project=project3, date=date(2015, 9, 21), duration=timedelta(hours=3))

        # create the invoices
        invoice1 = InvoiceFactory.create(client=client1, date=date(2015, 9, 30))
        invoice2 = InvoiceFactory.create(client=client1, date=date(2015, 10, 31))

        # generate the invoices and check that the correct number of lines are created
        invoice1.generate()
        self.assertIsNotNone(invoice1.generated)
        self.assertEqual(invoice1.invoice_number, '201500001')
        self.assertEqual(InvoiceItem.objects.count(), 3)

        # check the financial data
        for item in InvoiceItem.objects.all():
            self.assertEqual(item.rate, item.project.base_rate)

        expected_vat_free_total = project1.base_rate * 4 + project2.base_rate * 5
        self.assertEqual(invoice1.total_no_vat, expected_vat_free_total)
        self.assertEqual(invoice1.total_with_vat, expected_vat_free_total * Decimal('1.24'))

        invoice2.generate()
        self.assertEqual(InvoiceItem.objects.count(), 4)

    @freeze_time('2015-10-02')
    def test_multiple_generate_idempotent(self):
        client = ClientFactory.create()
        WorkEntryFactory.create(project__client=client, date=date(2015, 9, 14), duration=timedelta(hours=4))

        invoice = InvoiceFactory.create(client=client, date=date(2015, 9, 30))
        invoice.generate()

        items = InvoiceItem.objects.all()
        self.assertEqual(items.count(), 1)

        # second call may not generate new items
        invoice.generate()
        self.assertEqual(items.count(), 1)

    def test_incrementing_invoice_number(self):
        client1, client2 = ClientFactory.create_batch(2)

        with freeze_time('2015-10-02'):
            invoice1 = InvoiceFactory.create(client=client1, date=date(2015, 9, 30))
            invoice1bis = InvoiceFactory.create(client=client1, date=date(2015, 9, 30))
            invoice1bis.delete()
            invoice2 = InvoiceFactory.create(client=client2, date=date(2015, 10, 31))

            self.assertGreater(invoice2.pk-1, invoice1.pk)

            invoice1.generate_invoice_number()
            invoice2.generate_invoice_number()

            this_year = str(timezone.now().year)

        self.assertEqual(invoice1.invoice_number, '201500001'.format(this_year))
        self.assertEqual(invoice2.invoice_number, '201500002'.format(this_year))

        with freeze_time('2016-02-23'):
            invoice3 = InvoiceFactory.create(client=client2, date=date(2016, 2, 15))
            invoice3.generate_invoice_number()
        self.assertEqual(invoice3.invoice_number, '201600003'.format(this_year))

    @freeze_time('2015-10-21')
    def test_generate_invoice_flat_fee(self):
        project = ProjectFactory.create(flat_fee=3500)
        invoice = InvoiceFactory.create(client=project.client, date=date(2015, 10, 15))
        InvoiceItemFactory.create(
            invoice=invoice, project=project,
            rate=3500, amount=1, tax_rate=TaxRates.standard,
            source_object=project
        )

        self.assertFalse(invoice.invoice_number)
        invoice.generate()
        self.assertEqual(invoice.invoice_number, '201500001')
        self.assertEqual(invoice.get_totals(), {
            'base__sum': Decimal('3500'),
            'tax__sum': Decimal('840')
        })

    @override_settings(SITE_COUNTRY='NL')
    def test_international_vat(self):
        invoice = InvoiceFactory.create(client__country='BE', date=date(2015, 10, 15))
        self.assertTrue(invoice.vat_reverse_charge)

        invoice2 = InvoiceFactory.create(client__country='NL', date=date(2015, 10, 15))
        self.assertFalse(invoice2.vat_reverse_charge)


class InvoiceItemTemplateTests(TestCase):
    def setUp(self):
        self.client = ClientFactory(is_default=True)
        self.project = ProjectFactory(client=self.client)

    def test_generate_bills_templates_for_default_client(self):
        InvoiceItemTemplate.objects.create(project=self.project, title='Monthly rate', rate=Decimal('3500'))
        invoice = InvoiceFactory.create(client=self.client, date=date(2026, 1, 1))

        invoice.generate()

        item = invoice.invoiceitem_set.get()
        self.assertEqual(item.remarks, 'Monthly rate')
        self.assertEqual(item.rate, Decimal('3500'))
        self.assertEqual(item.amount, 1)

    def test_generate_skips_templates_for_non_default_client(self):
        client = ClientFactory()
        project = ProjectFactory(client=client)
        InvoiceItemTemplate.objects.create(project=project, title='Monthly rate')
        invoice = InvoiceFactory.create(client=client, date=date(2026, 1, 1))

        invoice.generate()

        self.assertFalse(invoice.invoiceitem_set.exists())

    def test_two_invoices_same_date_each_bill_their_template_lines(self):
        InvoiceItemTemplate.objects.create(project=self.project, title='Monthly rate', rate=Decimal('3500'))
        first = InvoiceFactory.create(client=self.client, date=date(2026, 1, 1))
        second = InvoiceFactory.create(client=self.client, date=date(2026, 1, 1))

        first.generate()
        second.generate()

        self.assertEqual(first.invoiceitem_set.get().remarks, 'Monthly rate')
        self.assertEqual(second.invoiceitem_set.get().remarks, 'Monthly rate')

    def test_regenerate_keeps_number_and_manual_lines(self):
        InvoiceItemTemplate.objects.create(project=self.project, title='Monthly rate', rate=Decimal('3500'))
        invoice = InvoiceFactory.create(client=self.client, date=date(2026, 1, 1))
        invoice.generate()
        invoice_number = invoice.invoice_number
        InvoiceItem.objects.create(
            invoice=invoice, project=self.project, rate=Decimal('10'), amount=1, remarks='Manual line')

        invoice.regenerate()

        invoice.refresh_from_db()
        self.assertEqual(invoice.invoice_number, invoice_number)
        self.assertEqual(invoice.invoiceitem_set.filter(remarks='Manual line').count(), 1)
        self.assertEqual(invoice.invoiceitem_set.filter(remarks='Monthly rate').count(), 1)
