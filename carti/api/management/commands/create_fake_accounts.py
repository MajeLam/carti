import random
import string
from django.core.management.base import BaseCommand
from api.models import BankAccount

# python manage.py create_fake_accounts 10
class Command(BaseCommand):
    help = "Génère automatiquement des comptes bancaires avec des soldes positifs et négatifs"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Nombre de comptes à créer")

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        created_accounts = []

        for _ in range(count):
            account_number = ''.join(random.choices(string.digits, k=10))
            owner = f"Client-{random.randint(1000, 9999)}"
            balance = round(random.uniform(-300, 15500), 2)  # Générer un solde entre -300 et 15500
            currency = "EUR"

            account = BankAccount.objects.create(
                account_number=account_number,
                owner=owner,
                balance=balance,
                currency=currency
            )
            created_accounts.append(account)

        self.stdout.write(self.style.SUCCESS(f"{count} comptes bancaires générés avec succès !"))
