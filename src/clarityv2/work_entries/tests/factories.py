from datetime import timedelta

import factory

from clarityv2.accounts.tests.factories import UserFactory
from clarityv2.crm.tests.factories import ProjectFactory

from ..models import WorkEntry


class WorkEntryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    duration = timedelta(hours=1)

    class Meta:
        model = WorkEntry
