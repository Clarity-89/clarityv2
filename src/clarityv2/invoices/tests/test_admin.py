from datetime import date

from django.test import TestCase
from django.urls import reverse

from clarityv2.accounts.models import User
from clarityv2.crm.tests.factories import ClientFactory


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
