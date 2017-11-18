class OrderingMixin:
    default_ordering = None  # must be specified in subclass
    table_headers = None  # must be specified in subclass

    def get_ordering(self):
        self.direction = self.request.GET.get('direction', 'asc')
        ordering = self.request.GET.get('order_by', self.get_default_ordering())
        if self.direction == "desc":
            ordering = "-" + ordering

        return ordering

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['direction'] = self.direction
        context['order'] = self.get_ordering().replace('-', '')
        context['headers'] = self.get_table_headers()

        return context

    def get_default_ordering(self):
        return self.default_ordering

    def get_table_headers(self):
        return self.table_headers
