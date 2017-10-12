from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = 'clarityv2.utils'

    def ready(self):
        from . import checks  # noqa
