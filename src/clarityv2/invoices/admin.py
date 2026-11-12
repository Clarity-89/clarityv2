from datetime import date

from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from privates.admin import PrivateMediaMixin

from clarityv2.crm.models import Client

from .models import Invoice, InvoiceItem, InvoiceItemTemplate
from .utils import render_invoice_pdf


def regenerate_invoices(modeladmin, request, queryset):
    for invoice in queryset:
        invoice.regenerate()


regenerate_invoices.short_description = _("Regenerate invoice details")


def render_pdf(modeladmin, request, queryset):
    for invoice in queryset:
        render_invoice_pdf(request, invoice)


render_pdf.short_description = _("Generate invoice pdfs")


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(PrivateMediaMixin, admin.ModelAdmin):
    list_display = ('client', 'date', 'due_date', 'received', 'invoice_number',
                    'created', 'n_items', 'generated', 'invoice_items')
    list_filter = ('client', 'date', 'due_date', 'received')
    search_fields = ('invoice_number',)
    private_media_fields = ('pdf',)
    inlines = [InvoiceItemInline]
    actions = [regenerate_invoices, render_pdf]

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        default_client = Client.get_default()
        if default_client is not None:
            initial.setdefault('client', default_client.pk)
        initial.setdefault('date', date.today())
        return initial

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if not change:
            # Generate after inlines are saved so manual items are part of the invoice.
            form.instance.generate()

    def get_queryset(self, request=None):
        return super().get_queryset(request=request).annotate(n_items=Count('invoiceitem'))

    def n_items(self, obj):
        return obj.n_items

    n_items.short_description = _('# invoice items')

    def invoice_items(self, obj):
        url = reverse('admin:invoices_invoiceitem_changelist')
        return format_html('<a href="{}?invoice={}">{}</a>', url, obj.pk, _('invoice items'))

    invoice_items.short_description = _('invoice items')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'project', 'rate', 'amount', 'tax_rate')
    list_filter = ('invoice__client', 'project')


@admin.register(InvoiceItemTemplate)
class InvoiceItemTemplateAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'duration', 'rate')
    list_filter = ('project__client', 'project')
    search_fields = ('title',)
