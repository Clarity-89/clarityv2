from django.views.generic import ListView, DetailView

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.all()
    template_name = 'blog/list.html'
    context_object_name = 'blog_posts'
    paginate_by = 15

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.published()


class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.published()
    template_name = 'blog/detail.html'
    context_object_name = 'blog_post'
