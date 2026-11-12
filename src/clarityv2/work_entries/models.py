import datetime
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from clarityv2.invoices.constants import TWO_DIGITS


class WorkEntry(models.Model):
    project = models.ForeignKey('crm.Project', on_delete=models.PROTECT)
    date = models.DateField(_('date'), default=datetime.date.today)
    duration = models.DurationField(_('duration'), default=datetime.timedelta(hours=1))
    rate = models.DecimalField(
        _('rate'), max_digits=10, decimal_places=2, null=True, blank=True,
        help_text=_('Overrides the project rate for this entry.'),
    )

    notes = models.TextField(blank=True)
    source_invoice = models.ForeignKey(
        'invoices.Invoice', null=True, blank=True, editable=False,
        on_delete=models.CASCADE, related_name='default_work_entries',
    )

    class Meta:
        verbose_name = _('work entry')
        verbose_name_plural = _('work entries')
        ordering = ('-date',)

    def __str__(self):
        return '{project} - {date} - {duration}'.format(project=self.project, date=self.date, duration=self.duration)

    @property
    def total(self):
        rate = self.rate or self.project.base_rate
        if rate:
            total_seconds = int(self.duration.total_seconds())
            duration = total_seconds / 3600
            return (Decimal(round(float(duration), 2)) * rate).quantize(TWO_DIGITS)
        return self.project.flat_fee


class WorkEntryTemplate(models.Model):
    project = models.ForeignKey('crm.Project', on_delete=models.CASCADE, related_name='work_entry_templates')
    title = models.CharField(_('title'), max_length=255, help_text=_('Invoice line description.'))
    duration = models.DurationField(_('duration'), default=datetime.timedelta(hours=1))
    rate = models.DecimalField(
        _('rate'), max_digits=10, decimal_places=2, null=True, blank=True,
        help_text=_('Overrides the project rate for this entry.'),
    )

    class Meta:
        verbose_name = _('work entry template')
        verbose_name_plural = _('work entry templates')
        ordering = ('project', 'title')

    def __str__(self):
        return '{project} - {title}'.format(project=self.project, title=self.title)
