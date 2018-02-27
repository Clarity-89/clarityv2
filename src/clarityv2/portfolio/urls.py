from django.conf.urls import url

from .views import EntryDetailView, EntryListView

urlpatterns = [
    url(r'^$', EntryListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/log/', EntryDetailView.as_view(), name='detail'),
]
