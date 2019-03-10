from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path(r'admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('clarityv2.accounts.urls', namespace='accounts')),
    path('admin/password_reset/', auth_views.PasswordResetView, name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView, name='password_reset_done'),
    path('admin/hijack/', include('hijack.urls')),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView, name='password_reset_confirm'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('invoices/', include(('clarityv2.invoices.urls', 'invoices'), namespace='invoices')),
    path('reset/done/', auth_views.PasswordResetCompleteView, name='password_reset_complete'),
    path('portfolio/', include(('clarityv2.portfolio.urls', 'portfolio'), namespace='portfolio')),
    path('work_entries/', include(('clarityv2.work_entries.urls', 'work_entries'), namespace='work_entries')),

    # Simply show the master template.
    path(r'', include(('clarityv2.homepage.urls', 'home'), namespace='home')),
]

# NOTE: The staticfiles_urlpatterns also discovers static files (ie. no need to run collectstatic). Both the static
# folder and the media folder are only served via Django if DEBUG = True.
urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
                       path(r'__debug__/', include(debug_toolbar.urls)),
                   ] + static(settings.PRIVATE_MEDIA_URL, document_root=settings.PRIVATE_MEDIA_ROOT)
