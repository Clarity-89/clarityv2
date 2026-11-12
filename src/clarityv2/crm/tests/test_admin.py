from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from clarityv2.accounts.models import User
from clarityv2.invoices.models import InvoiceItemTemplate

from .factories import ClientFactory, ProjectFactory


class InvoiceItemTemplateInlineTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')

    def setUp(self):
        self.client.force_login(self.user)

    def _formset(self, project):
        response = self.client.get(reverse('admin:crm_project_change', args=[project.pk]))
        self.assertEqual(response.status_code, 200)
        inline = next(
            inline for inline in response.context['inline_admin_formsets']
            if inline.opts.model is InvoiceItemTemplate
        )
        return inline.formset

    def test_new_row_prefills_rate_from_flat_fee(self):
        project = ProjectFactory(client=ClientFactory(), flat_fee=Decimal('12100'))

        formset = self._formset(project)

        self.assertEqual(formset.empty_form['rate'].value(), Decimal('12100.00'))

    def test_new_row_falls_back_to_base_rate(self):
        project = ProjectFactory(client=ClientFactory(), base_rate=Decimal('60'))

        formset = self._formset(project)

        self.assertEqual(formset.empty_form['rate'].value(), Decimal('60.00'))

    def test_existing_rows_keep_their_rate(self):
        project = ProjectFactory(client=ClientFactory(), flat_fee=Decimal('12100'))
        InvoiceItemTemplate.objects.create(project=project, title='Support', rate=Decimal('120'))

        formset = self._formset(project)

        self.assertEqual(formset.forms[0]['rate'].value(), Decimal('120.00'))
        self.assertEqual(formset.empty_form['rate'].value(), Decimal('12100.00'))
