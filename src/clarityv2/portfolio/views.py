from django.views.generic import ListView, DetailView

from .models import Entry


class EntryListView(ListView):
    model = Entry
    queryset = Entry.objects.published
    template_name = 'portfolio/list.html'


class EntryDetailView(DetailView):
    model = Entry
    queryset = Entry.objects.published
    template_name = 'portfolio/detail.html'
