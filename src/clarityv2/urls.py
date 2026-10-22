from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from clarityv2.invoices.dev_views import InvoicePDFTestView

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Static and media files are only served by Django when DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
                                                  show_indexes=True)
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
                       path(r'__debug__/', include(debug_toolbar.urls)),
                   ] + static(settings.PRIVATE_MEDIA_URL, document_root=settings.PRIVATE_MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path(
            "dev/invoices/<int:pk>/pdf/",
            InvoicePDFTestView.as_view(),
            name="dev-invoice-pdf",
        ),
    ]
