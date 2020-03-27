import datetime
from datetime import timedelta

from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin

from .models import WorkEntry


class CustomDateTimeFilter(DateFieldListFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        now = timezone.now()
        # When time zone support is enabled, convert "now" to the user's time
        # zone so Django's definition of "Today" matches what the user expects.
        if timezone.is_aware(now):
            now = timezone.localtime(now)

        today = now.date()
        last_year_begin = today.replace(year=today.year - 1, month=1, day=1)
        last_year_end = today.replace(year=today.year, month=1, day=1)
        self.links += ((
            (_('Last year'), {
                self.lookup_kwarg_since: str(last_year_begin),
                self.lookup_kwarg_until: str(last_year_end),
            }),
        ))


@admin.register(WorkEntry)
class WorkEntryAdmin(ImportExportActionModelAdmin):
    list_display = ('date', 'duration', 'project', 'notes')
    list_filter = ('project__client', 'project', ('date', CustomDateTimeFilter))
    search_fields = ('notes',)
    change_list_template = 'admin/work_entries/workentry/change_list.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=None)

        if hasattr(response, 'context_data'):
            cl = response.context_data.get('cl')
            if cl:
                queryset = cl.get_queryset(request)
                duration = (queryset.aggregate(Sum('duration'))['duration__sum']) or timedelta()
                response.context_data['total_duration'] = duration.total_seconds() / 3600
        return response
