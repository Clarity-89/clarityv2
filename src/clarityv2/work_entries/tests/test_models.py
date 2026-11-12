from datetime import timedelta
from decimal import Decimal

from django.test import TestCase

from clarityv2.crm.tests.factories import ClientFactory, ProjectFactory
from clarityv2.invoices.tests.factories import InvoiceFactory

from ..models import WorkEntry, WorkEntryTemplate


class DefaultWorkEntryTests(TestCase):
    def test_invoice_for_default_client_creates_template_entries(self):
        client = ClientFactory(is_default=True)
        project = ProjectFactory(client=client)
        WorkEntryTemplate.objects.create(project=project, title='Monthly rate', rate=Decimal('3500'))
        WorkEntryTemplate.objects.create(project=project, title='Support', rate=Decimal('120'))

        invoice = InvoiceFactory(client=client)

        entries = WorkEntry.objects.filter(source_invoice=invoice).order_by('notes')
        self.assertEqual([entry.notes for entry in entries], ['Monthly rate', 'Support'])
        self.assertEqual([entry.rate for entry in entries], [Decimal('3500'), Decimal('120')])
        self.assertEqual({entry.duration for entry in entries}, {timedelta(hours=1)})

    def test_invoice_for_non_default_client_does_not_create_entries(self):
        client = ClientFactory()
        project = ProjectFactory(client=client)
        WorkEntryTemplate.objects.create(project=project, title='Monthly rate')

        invoice = InvoiceFactory(client=client)

        self.assertFalse(WorkEntry.objects.filter(source_invoice=invoice).exists())
