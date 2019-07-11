from django.views.generic import ListView, DetailView

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.published
    template_name = 'blog_post/list.html'
    context_object_name = 'blog_post'
    paginate_by = 10


class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.published
    template_name = 'blog_post/detail.html'
    context_object_name = 'blog_post'
