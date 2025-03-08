from django.db import models

class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    owner = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")

    def __str__(self):
        return f"{self.account_number} - {self.owner}"

class CreditCard(models.Model):
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="cards")

    def __str__(self):
        return f"Card {self.card_number} for {self.account.owner}"