from django.urls import path

from .views import DashboardView

app_name = 'accounts'
urlpatterns = [
    path('projects', DashboardView.as_view(), name='projects')
]
