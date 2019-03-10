from django.urls import path

from .views import InvoiceDetailView, InvoiceDetailPDFView


urlpatterns = [
    path('invoice/<int:invoice_number>)/', InvoiceDetailView.as_view(), name='detail'),
    path('invoice/<int:invoice_number>/pdf/', InvoiceDetailPDFView.as_view(), name='detail-pdf'),
]
