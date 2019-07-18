from django.views.generic import ListView, DetailView

from .models import Entry


class EntryListView(ListView):
    model = Entry
    queryset = Entry.objects.published()
    template_name = 'portfolio/list.html'
    context_object_name = 'portfolio'


class EntryDetailView(DetailView):
    model = Entry
    queryset = Entry.objects.published()
    template_name = 'portfolio/detail.html'
    context_object_name = 'entry'
