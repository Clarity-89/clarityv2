import factory

from clarityv2.accounts.tests.factories import UserFactory
from clarityv2.crm.tests.factories import ProjectFactory
from ..models import WorkEntry


class WorkEntryFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = WorkEntry
