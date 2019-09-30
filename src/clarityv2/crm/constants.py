from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class Currencies(DjangoChoices):
    usd = ChoiceItem('usd', _('USD'))
    euro = ChoiceItem('euro', _('u"\u20AC"'))
