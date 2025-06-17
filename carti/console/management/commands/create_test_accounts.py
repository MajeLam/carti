from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import BankAccount
import random
from faker import Faker
from decimal import Decimal
import string

User = get_user_model()
fake = Faker('fr_FR')

class Command(BaseCommand):
    help = 'Crée des comptes bancaires de test'

    def generate_account_number(self):
        """Génère un numéro de compte unique"""
        while True:
            account_number = ''.join(random.choices(string.digits, k=10))
            if not BankAccount.objects.filter(account_number=account_number).exists():
                return account_number

    def handle(self, *args, **kwargs):
        # Créer un utilisateur de test s'il n'existe pas
        test_user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'username': 'testuser',
                'phone_number': '+33612345678',
                'address': '123 rue Test',
                'date_of_birth': '1990-01-01'
            }
        )
        
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write(self.style.SUCCESS(f'Utilisateur de test créé : {test_user.email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Utilisateur de test existant : {test_user.email}'))

        # Créer 10 comptes bancaires
        for i in range(10):
            account_number = self.generate_account_number()
            balance = Decimal(str(random.uniform(1000, 100000)))
            
            account = BankAccount.objects.create(
                account_number=account_number,
                owner=test_user,
                balance=balance,
                currency='EUR'  # Toujours EUR
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Compte créé : {account.account_number} - Solde : {account.balance} {account.currency}'
                )
            )

        self.stdout.write(self.style.SUCCESS('10 comptes bancaires ont été créés avec succès')) 