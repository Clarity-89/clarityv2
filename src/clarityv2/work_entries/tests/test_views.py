from django.core.urlresolvers import reverse

from django_webtest import WebTest

from clarityv2.accounts.tests.factories import UserFactory
from clarityv2.crm.tests.factories import ClientFactory, ProjectFactory, ContactFactory
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
        WorkEntryFactory.create(project=project1, user=self.user1)
        project2 = ProjectFactory.create(client=self.client2)
        WorkEntryFactory.create(project=project2, user=self.user2)
        WorkEntryFactory.create(project=project2, user=self.user2)

        response1 = self.app.get(reverse('work_entries:list', kwargs={'project_slug': project1.slug}))
        self.assertQuerysetEqual(len(response1.context['work_entries']), 1)
