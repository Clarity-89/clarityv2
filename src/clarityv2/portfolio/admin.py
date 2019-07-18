from django.contrib import admin

from .models import Entry


@admin.register(Entry)
class PortfolioEntryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description', 'published', 'order', 'url')
