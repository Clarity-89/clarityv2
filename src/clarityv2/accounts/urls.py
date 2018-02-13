from django.conf.urls import url

from .views import DashboardView

app_name = 'accounts'
urlpatterns = [
    url(r'^projects/$', DashboardView.as_view(), name='projects')
]
