from datetime import timedelta

from django.contrib import admin
from django.db.models import F, Sum

from import_export.admin import ImportExportActionModelAdmin

from .models import WorkEntry


@admin.register(WorkEntry)
class WorkEntryAdmin(ImportExportActionModelAdmin):
    list_display = ('date', 'duration', 'project', 'notes')
    list_filter = ('project__client', 'project', 'date')
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