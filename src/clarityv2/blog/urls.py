from django.urls import path

from .views import BlogPostDetailView, BlogPostListView, BlogFeed

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('feed/', BlogFeed(), name='feed'),
    path('<slug>/', BlogPostDetailView.as_view(), name='detail'),
]
