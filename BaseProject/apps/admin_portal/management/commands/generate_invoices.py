from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from BaseProject.apps.admin_portal.models import Invoices


class Command(BaseCommand):
    help = "Genera facturas falsas para pruebas usando Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            '--total',
            type=int,
            default=10,
            help='Número de facturas a generar (por defecto: 10)',
        )

    def handle(self, *args, **options):
        fake = Faker('es_MX')
        total = options['total']

        # addresses = list(Address.objects.all())
        # if not addresses:
        #     self.stdout.write(self.style.ERROR("⚠️ No hay direcciones disponibles en Address."))
        #     return

        for _ in range(total):
            invoice = Invoices.objects.create(
                folio=f"F-{fake.unique.random_int(min=1000, max=9999)}",
                date=fake.date_between(start_date='-3y', end_date='today'),
                amount=round(random.uniform(100.0, 10000.0), 2),
                client_name=fake.name(),
                client_address=fake.address(),
                client_email=fake.email(),
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Creada factura: {invoice.folio} ({invoice.client_name})"))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 {total} facturas generadas exitosamente."))
