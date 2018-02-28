from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description', 'published', 'order', 'url')
