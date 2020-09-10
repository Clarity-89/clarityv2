from django.views.generic import DetailView, ListView
from django.contrib.syndication.views import Feed

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
    queryset = BlogPost.objects.all()
    template_name = 'blog/detail.html'
    context_object_name = 'blog_post'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.published()


class BlogFeed(Feed):
    title = "Latest blog posts"
    link = "/feed/"
    description = "Blog posts about interesting stuff around web development"

    def items(self):
        return BlogPost.objects.all()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
