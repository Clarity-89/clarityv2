import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class WorkEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    project = models.ForeignKey('crm.Project')
    date = models.DateField(_('date'), default=datetime.date.today)
    duration = models.DurationField(_('duration'))

    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = _('work entry')
        verbose_name_plural = _('work entries')
        ordering = ('-date',)

    def __str__(self):
        return '{project} - {date} - {duration}'.format(project=self.project, date=self.date, duration=self.duration)