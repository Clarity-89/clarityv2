import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.functions import ExtractYear
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from clarityv2.crm.models import Project

from .mixins import OrderingMixin
from .models import WorkEntry


class WorkEntryList(LoginRequiredMixin, OrderingMixin, ListView):
    model = WorkEntry
    context_object_name = 'work_entries'
    paginate_by = 25
    default_ordering = '-date'
    table_headers = [{'name': 'notes', 'label': _('Notes'), 'sortable': False},
                     {'name': 'date', 'label': _('Date'), 'sortable': True},
                     {'name': 'duration', 'label': _('Duration (hours)'), 'sortable': True},
                     {'name': 'price', 'label': _('Price'), 'sortable': False}]

    def _get_project_filters(self):
        return {
            'slug': self.kwargs['project_slug'],
            'client__contacts__user': self.request.user
        }

    def get_context_data(self, **kwargs):
        qs = Project.objects.filter(**self._get_project_filters())
        kwargs['project'] = get_object_or_404(qs)
        duration = WorkEntry.objects.aggregate(Sum('duration'))['duration__sum']
        kwargs['total_hours'] = duration.total_seconds() / 3600
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        now = datetime.datetime.now()
        qs = super().get_queryset()
        filters = {'project__%s' % key: value for key, value in self._get_project_filters().items()}
        return qs.annotate(year=ExtractYear('date')).filter(**filters).filter(year=now.year)
