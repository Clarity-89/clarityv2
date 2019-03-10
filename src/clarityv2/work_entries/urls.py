from django.urls import path

from .views import WorkEntryList

app_name = 'work_entries'
urlpatterns = [
    path('<project_slug>)/log/', WorkEntryList.as_view(), name='list'),
]
