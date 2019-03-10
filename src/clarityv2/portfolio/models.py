from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField


class EntryQueryset(models.QuerySet):

    def published(self):
        return self.filter(published=True)


class Entry(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(_('slug'), populate_from='name', unique=True)
    image = models.ImageField(_('image'), blank=True, upload_to='portfolio')
    description = RichTextField(blank=True)

    order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(_('published'), default=True)
    url = models.URLField(_('URL'), null=True)
    objects = EntryQueryset.as_manager()

    class Meta:
        verbose_name = _('portfolio entry')
        verbose_name_plural = _('portfolio entries')
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portfolio:detail', kwargs={'slug': self.slug})
