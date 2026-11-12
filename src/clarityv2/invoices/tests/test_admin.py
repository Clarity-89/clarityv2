from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from clarityv2.accounts.models import User
from clarityv2.crm.tests.factories import ClientFactory, ProjectFactory

from ..models import Invoice, InvoiceItemTemplate


class InvoiceAdminDefaultsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        cls.default_client = ClientFactory(is_default=True)

    def setUp(self):
        self.client.force_login(self.user)

    def test_add_form_preselects_default_client_and_today(self):
        response = self.client.get(reverse('admin:invoices_invoice_add'))

        self.assertEqual(response.status_code, 200)
        form = response.context['adminform'].form
        self.assertEqual(form.initial['client'], self.default_client.pk)
        self.assertEqual(form['date'].value(), date.today())

    def test_add_form_generates_invoice(self):
        project = ProjectFactory(client=self.default_client)
        InvoiceItemTemplate.objects.create(project=project, title='Monthly rate', rate=Decimal('3500'))

        response = self.client.post(reverse('admin:invoices_invoice_add'), {
            'client': self.default_client.pk,
            'date': date.today().isoformat(),
            'invoiceitem_set-TOTAL_FORMS': '0',
            'invoiceitem_set-INITIAL_FORMS': '0',
            'invoiceitem_set-MIN_NUM_FORMS': '0',
            'invoiceitem_set-MAX_NUM_FORMS': '1000',
        })

        self.assertEqual(response.status_code, 302)
        invoice = Invoice.objects.get()
        self.assertIsNotNone(invoice.generated)
        self.assertTrue(invoice.invoice_number)
        item = invoice.invoiceitem_set.get()
        self.assertEqual(item.remarks, 'Monthly rate')
        self.assertEqual(item.rate, Decimal('3500'))
