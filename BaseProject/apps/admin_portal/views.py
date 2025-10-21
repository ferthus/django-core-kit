from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render

import django_tables2 as tables
from .models import Invoices


# ==> tables
class InvoiceTable(tables.Table):
    class Meta:
        model = Invoices
        template_name = "django_tables2/bootstrap.html"
        fields = ("folio", "date")


# ==> filters
import django_filters
from .models import Invoices


class InvoiceFilterSet(django_filters.FilterSet):
  q = django_filters.CharFilter(
    method='search',
    label=_('Search')
  )

  class Meta:
    model = Invoices
    fields = ("folio", "date")

  def search(self, queryset, name, value):
    if not value.strip():
      return queryset
    return queryset.filter(
      Q(folio__icontains=value) |
      Q(client_name__icontains=value)
    ).distinct()


# ==> views
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from BaseProject.apps.admin_portal.policy import invoice_policy
from BaseProject.core.permissions import PermissionCheckedMixin


class InvoiceListView(PermissionCheckedMixin, SingleTableMixin, FilterView):
    model = Invoices
    queryset = Invoices.objects.all()
    table_class = InvoiceTable
    filterset_class = InvoiceFilterSet
    permission_policy = invoice_policy
    permission_required = ["create_invoice"]
    template_name = 'admin_portal/tables/example.html'

    def get_table_pagination(self, table):
      return {'per_page': 20}

    def get(self, request, *args, **kwargs):
        self.filterset = self.filterset_class(request.GET, self.queryset, request=request)
        if (
            not self.filterset.is_bound
            or self.filterset.is_valid()
            or not self.get_strict()
        ):
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        context = self.get_context_data(
            filter=self.filterset,
            object_list=self.object_list
        )
        if request.htmx:
          return render(request, 'htmx/table.html', context)
        return self.render_to_response(context)
