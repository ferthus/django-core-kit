from django_tables2 import SingleTableView

from BaseProject.core.base_policy import BasePermissionPolicy
from BaseProject.apps.admin_portal.models import Invoices


class InvoicePolicyTable(BasePermissionPolicy):
    ...

invoice_policy = BasePermissionPolicy(Invoices)
