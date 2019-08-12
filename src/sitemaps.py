from django.contrib.sitemaps import Sitemap
from clarityv2.blog.models import BlogPost
from django.urls import reverse


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return BlogPost.objects.published()

    def lastmod(self, obj):
        return obj.pub_date


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ['contact', 'about', 'portfolio:list', 'home:home', 'blog:list']

    def location(self, item):
        return reverse(item)
