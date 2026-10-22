from django.db import models
from django.utils.translation import gettext_lazy as _


class Currencies(models.TextChoices):
    usd = 'usd', _('USD')
    euro = 'euro', _('\u20AC')
