from django.urls import include, path

from BaseProject.apps.admin_portal.views import InvoiceListView


app_name = "admin_portal"

urlpatterns = [
    path('', InvoiceListView.as_view(), name='home'),
]
