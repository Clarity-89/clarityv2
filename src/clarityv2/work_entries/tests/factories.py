from datetime import timedelta

import factory

from clarityv2.crm.tests.factories import ProjectFactory

from ..models import WorkEntry


class WorkEntryFactory(factory.django.DjangoModelFactory):
    project = factory.SubFactory(ProjectFactory)
    duration = timedelta(hours=1)

    class Meta:
        model = WorkEntry
