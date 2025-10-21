from django.db import models


class Invoices(models.Model):
  folio = models.CharField(max_length=120)
  date = models.DateField()
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  client_name = models.CharField(max_length=100)
  client_address = models.CharField(max_length=100)
  client_email = models.EmailField()


  class Meta:
    default_permissions = ()
    permissions = [
      ("create_invoice", "Crear facturacion"),
      ("create_invoice_public_general", "Crear factura publico general"),
      ("cancel_invoice", "Cancelar facturacion"),
      ("cancel_invoice_public_general", "Crear factura publico general"),
    ]
