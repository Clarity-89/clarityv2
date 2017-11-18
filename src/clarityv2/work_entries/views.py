from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.utils.translation import ugettext_lazy as _
from clarityv2.crm.models import Project

from .models import WorkEntry
from .mixins import OrderingMixin


class WorkEntryList(LoginRequiredMixin, OrderingMixin, ListView):
    model = WorkEntry
    context_object_name = 'work_entries'
    paginate_by = 25
    default_ordering = '-date'
    table_headers = [{'name': 'notes', 'label': _('Notes'), 'sortable': False},
                     {'name': 'date', 'label': _('Date'), 'sortable': True},
                     {'name': 'duration', 'label': _('Duration'), 'sortable': True}]

    def get_context_data(self, **kwargs):
        slug = self.kwargs['project_slug']
        kwargs['project'] = Project.objects.get(slug=slug)
        return super().get_context_data(**kwargs)
