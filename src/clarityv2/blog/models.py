from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class BlogPostQueryset(models.QuerySet):

    def published(self):
        return self.filter(published=True)

    def draft(self):
        return self.filter(published=False)


class BlogPost(models.Model):
    title = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name', unique=True)
    image = models.ImageField(_('image'), blank=True, upload_to='blog')
    text = RichTextField(blank=True)
    tags = TaggableManager()
    published = models.BooleanField(_('published'), default=False)
    objects = BlogPostQueryset.as_manager()

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('blog post')
        verbose_name_plural = _('blog post')
        ordering = ['created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post:detail', kwargs={'slug': self.slug})
