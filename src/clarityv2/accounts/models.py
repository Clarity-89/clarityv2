from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from solo.models import SingletonModel

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Use the built-in user model.
    """
    username = models.CharField(
        _('username'), max_length=150,
        unique=True, help_text=_('Required. 150 characters or fewer.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class AdminUser(SingletonModel):
    company_name = models.CharField(_('company name'), max_length=255, blank=True)
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField(_('phone number'), max_length=150)
    address_street = models.CharField(_('street'), max_length=255, blank=True)
    house_number = models.CharField(_("house number"), max_length=10, blank=True)
    city = models.CharField(_('city'), max_length=64, blank=True)
    country = CountryField(_('country'), blank=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True)
    business_id = models.CharField(_('business ID'), max_length=50, blank=True)
    vat_number = models.CharField(_('VAT number'), max_length=50, blank=True)
    iban = models.CharField(_('iban'), max_length=50, blank=True)
    bank = models.CharField(_('bank'), max_length=50, blank=True)
    bank_branch = models.CharField(_('bank branch'), max_length=50, blank=True)
    swift = models.CharField(_('swift'), max_length=50, blank=True)

    class Meta:
        verbose_name = _('admin user')
        verbose_name_plural = _('admin users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_entity_name(self):
        """
        Returns company name or person full name
        """
        if self.company_name is not None:
            return self.company_name
        return self.get_full_name()

    def get_full_street_address(self):
        address = "{} {}".format(self.address_street, self.house_number)

        return address.strip()
