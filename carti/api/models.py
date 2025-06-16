from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Ajout des related_name pour résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class BankAccount(models.Model):
    account_number = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.owner.email}"

class CreditCard(models.Model):
    CARD_TYPES = (
        ('PHYSICAL', 'Carte Physique'),
        ('VIRTUAL', 'Carte Virtuelle'),
    )
    
    card_number = models.CharField(max_length=16, unique=True)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="cards")
    card_type = models.CharField(max_length=10, choices=CARD_TYPES, default='PHYSICAL')
    is_active = models.BooleanField(default=True)
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Card {self.card_number} for {self.account.owner.email}"

class CardTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('PURCHASE', 'Achat'),
        ('WITHDRAWAL', 'Retrait'),
        ('TRANSFER', 'Transfert'),
    )
    
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, default='PENDING')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.card.card_number}"