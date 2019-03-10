from django.urls import path

from .views import EntryDetailView, EntryListView

urlpatterns = [
    path('', EntryListView.as_view(), name='list'),
    path('<slug>/log/', EntryDetailView.as_view(), name='detail'),
]
