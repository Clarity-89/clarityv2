from django.urls import reverse

from django_webtest import WebTest

from clarityv2.accounts.tests.factories import UserFactory
from clarityv2.crm.tests.factories import (
    ClientFactory, ContactFactory, ProjectFactory
)

from .factories import WorkEntryFactory


class WorkEntryTests(WebTest):

    def setUp(self):
        self.user1 = UserFactory.create(email='test1@me.com', username='t1')
        self.user2 = UserFactory.create(email='test2@me.com', username='t2')
        self.contact1 = ContactFactory.create(user=self.user1)
        self.contact2 = ContactFactory.create(user=self.user2)
        self.client1 = ClientFactory.create()
        self.client2 = ClientFactory.create()
        self.client1.contacts = [self.contact1]
        self.client2.contacts = [self.contact2]

    def test_entries_visibility(self):
        """
        Assert that users can see work entries for their projects.
        """
        project1 = ProjectFactory.create(client=self.client1)
        we1 = WorkEntryFactory.create(project=project1, user=self.user1)
        project2 = ProjectFactory.create(client=self.client2)
        we2 = WorkEntryFactory.create(project=project2, user=self.user2)
        we3 = WorkEntryFactory.create(project=project2, user=self.user2)

        page1 = self.app.get(reverse('work_entries:list', kwargs={'project_slug': project1.slug}), user=self.user1)
        self.assertEqual(page1.status_code, 200)
        entries = page1.context['work_entries']
        self.assertEqual(entries.count(), 1)
        self.assertEqual(entries.first(), we1)

        page2 = self.app.get(reverse('work_entries:list', kwargs={'project_slug': project2.slug}), user=self.user2)
        self.assertEqual(page1.status_code, 200)
        entries = page2.context['work_entries']
        self.assertEqual(entries.count(), 2)
        self.assertEqual(entries.first(), we2)

        # Accessing other users' projects is not possible
        page3 = self.app.get(reverse('work_entries:list', kwargs={'project_slug': project1.slug}), user=self.user2,
                             expect_errors=True)
        self.assertEqual(page3.status_code, 404)
