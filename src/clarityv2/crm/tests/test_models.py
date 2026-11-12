from django.test import TestCase

from ..models import Client
from .factories import ClientFactory


class ClientDefaultTests(TestCase):
    def test_get_default_returns_none_when_not_set(self):
        ClientFactory()

        self.assertIsNone(Client.get_default())

    def test_setting_a_new_default_clears_the_previous_one(self):
        previous = ClientFactory(is_default=True)
        current = ClientFactory()

        current.is_default = True
        current.save()

        previous.refresh_from_db()
        self.assertFalse(previous.is_default)
        self.assertEqual(Client.get_default(), current)
