from django.urls import path

from .views import BlogPostDetailView, BlogPostListView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('<slug>', BlogPostDetailView.as_view(), name='detail'),
]
