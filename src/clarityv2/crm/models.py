from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from django_countries.fields import CountryField
from djchoices import ChoiceItem, DjangoChoices
from phonenumber_field.modelfields import PhoneNumberField

from .constants import Currencies


class Contact(models.Model):
    """
    Contact details for a single contact from a Client.
    """

    label = models.CharField(_('label'), max_length=50, blank=True)
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email'))
    phone = PhoneNumberField(_('phone number'), blank=True)
    address = models.CharField(_('address'), max_length=255, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=255, blank=True)
    country = CountryField(default=settings.DEFAULT_COUNTRY, verbose_name=_('Country'))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name', unique=True)

    # global company contact details
    email = models.EmailField(_('email'))
    phone = PhoneNumberField(_('phone number'), blank=True)
    address = models.CharField(_('address'), max_length=255)
    postal_code = models.CharField(_('postal code'), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=255)
    country = CountryField(default=settings.DEFAULT_COUNTRY, verbose_name=_('Country'))
    language = models.CharField(_('language'), max_length=10, choices=settings.LANGUAGES, default='nl')

    # invoicing fields
    crn = models.CharField(_('registration number'), max_length=50, blank=True, help_text=_('Business ID'))
    vat_number = models.CharField(_('VAT number'), max_length=50, blank=True)

    contacts = models.ManyToManyField('Contact', blank=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("client")
        verbose_name_plural = _("clients")

    def __str__(self):
        return self.name


class TaxRates(DjangoChoices):
    no_vat = ChoiceItem(Decimal('0.00'), _('no vat'))
    standard = ChoiceItem(Decimal('0.24'), _('standard vat rate'))


class Project(models.Model):
    """
    Logical entity to group work entities under.

    Clients can have multiple projects going on.
    """

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name')

    # base financial information
    base_rate = models.DecimalField(_('hourly base rate'), max_digits=8, decimal_places=2, null=True, blank=True)
    flat_fee = models.DecimalField(_('flat fee'), max_digits=10, decimal_places=2, null=True, blank=True)
    vat = models.DecimalField(
        _('tax rate'), max_digits=4, decimal_places=2,
        choices=TaxRates.choices, default=TaxRates.no_vat
    )
    currency = models.CharField(_('currency'), max_length=20, choices=Currencies, default=Currencies.euro)

    class Meta:
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        unique_together = (
            ('client', 'slug'),
        )

    def __str__(self):
        return '{client} - {name}'.format(name=self.name, client=self.client)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        """
        Validate that at least one rate is provided.
        """
        if not self.base_rate and not self.flat_fee:
            raise ValidationError(_('Provide a base hourly rate or a flat fee.'))
