from django.test import TestCase
from django.urls import reverse

from clarityv2.accounts.models import User
from clarityv2.crm.tests.factories import ClientFactory, ProjectFactory


class WorkEntryAdminDefaultsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin')
        client = ClientFactory(is_default=True)
        cls.project = ProjectFactory(client=client, name='Default project')

    def setUp(self):
        self.client.force_login(self.user)

    def test_add_form_preselects_default_project_and_one_hour(self):
        response = self.client.get(reverse('admin:work_entries_workentry_add'))

        self.assertEqual(response.status_code, 200)
        form = response.context['adminform'].form
        self.assertEqual(form.initial['project'], self.project.pk)
        self.assertEqual(form['duration'].value(), '01:00:00')
