from django.shortcuts import render
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import random
import string
from .models import BankAccount, CreditCard, CardTransaction, User
from .serializers import (
    BankAccountSerializer, CreditCardSerializer, CardTransactionSerializer,
    VirtualCardRequestSerializer, UserSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur est propriétaire du compte
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

################## Authentication ####################

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({
            'error': 'Veuillez fournir un email et un mot de passe'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=email, password=password)
    
    if user is None:
        return Response({
            'error': 'Email ou mot de passe incorrect'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })

@api_view(['POST'])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################Home####################

def home(request):
    accounts = BankAccount.objects.all().order_by('-id')
    total_balance = sum(account.balance for account in accounts)
    num_accounts = BankAccount.objects.count()
    num_positive = BankAccount.objects.filter(balance__gt=0).count()
    num_negative = BankAccount.objects.filter(balance__lt=0).count()

    context = {
        'accounts': accounts,
        'total_balance': total_balance,
        'num_accounts': num_accounts,
        'num_positive': num_positive,
        'num_negative': num_negative,
    }
    return render(request, 'home.html', context)

##################Bank Account####################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_balance(request, account_number):
    try:
        account = BankAccount.objects.get(account_number=account_number)
        # Vérifier si l'utilisateur est propriétaire du compte
        if account.owner != request.user:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"account": account.account_number, "balance": account.balance, "currency": account.currency})
    except BankAccount.DoesNotExist:
        return Response({"error": "Compte introuvable"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_transaction(request):
    """
    Effectuer un dépôt ou un retrait
    Expects JSON: {"account_number": "123456", "amount": 100}
    """
    try:
        account = BankAccount.objects.get(account_number=request.data['account_number'])
        # Vérifier si l'utilisateur est propriétaire du compte
        if account.owner != request.user:
            return Response({"error": "Accès non autorisé"}, status=status.HTTP_403_FORBIDDEN)
            
        amount = (request.data['amount'])

        if amount < 0 and abs(amount) > account.balance:
            return Response({"error": "Fonds insuffisants"}, status=status.HTTP_400_BAD_REQUEST)

        account.balance += amount
        account.save()
        return Response({"message": "Transaction réussie", "new_balance": account.balance})

    except BankAccount.DoesNotExist:
        return Response({"error": "Compte introuvable"}, status=status.HTTP_404_NOT_FOUND)

class BankAccountListCreate(generics.ListCreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ne retourner que les comptes de l'utilisateur connecté
        return BankAccount.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Associer automatiquement le compte à l'utilisateur connecté
        serializer.save(owner=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_funds(request):
    """
    Effectuer un virement d'un compte à un autre.
    JSON attendu : {"from_account": "123456", "to_account": "654321", "amount": 50}
    """
    try:
        from_account_number = request.data.get('from_account')
        to_account_number = request.data.get('to_account')
        amount = (request.data.get('amount'))

        if amount <= 0:
            return Response({"error": "Le montant doit être positif"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():  # Assure que les opérations sont atomiques
            from_account = BankAccount.objects.select_for_update().get(account_number=from_account_number)
            to_account = BankAccount.objects.select_for_update().get(account_number=to_account_number)

            # Vérifier si l'utilisateur est propriétaire du compte source
            if from_account.owner != request.user:
                return Response({"error": "Accès non autorisé au compte source"}, status=status.HTTP_403_FORBIDDEN)

            if from_account.balance < amount:
                return Response({"error": "Fonds insuffisants"}, status=status.HTTP_400_BAD_REQUEST)

            # Effectuer le virement
            from_account.balance -= amount
            to_account.balance += amount

            from_account.save()
            to_account.save()

        return Response({
            "message": "Virement réussi",
            "from_account": from_account_number,
            "to_account": to_account_number,
            "transferred_amount": amount,
            "new_balance_from": from_account.balance,
            "new_balance_to": to_account.balance
        })

    except BankAccount.DoesNotExist:
        return Response({"error": "Un des comptes n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

###############credit card######################

@api_view(['GET'])
def list_cards(request, account_number):
    try:
        account = BankAccount.objects.get(account_number=account_number)
        cards = CreditCard.objects.filter(account=account)
        serializer = CreditCardSerializer(cards, many=True)
        return Response(serializer.data)
    except BankAccount.DoesNotExist:
        return Response({"error": "Compte introuvable"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_card(request):
    serializer = CreditCardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_card(request, card_number):
    try:
        card = CreditCard.objects.get(card_number=card_number)
        card.delete()
        return Response({"message": "Carte supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
    except CreditCard.DoesNotExist:
        return Response({"error": "Carte introuvable"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_virtual_card(request):
    """
    Crée une carte virtuelle pour un compte existant
    """
    serializer = VirtualCardRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        account = BankAccount.objects.get(
            account_number=serializer.validated_data['account_number'],
            owner=request.user
        )
    except BankAccount.DoesNotExist:
        return Response(
            {"error": "Compte introuvable ou non autorisé"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Générer un numéro de carte unique
    while True:
        card_number = ''.join(random.choices(string.digits, k=16))
        if not CreditCard.objects.filter(card_number=card_number).exists():
            break

    # Générer un CVV
    cvv = ''.join(random.choices(string.digits, k=3))

    # Date d'expiration (1 an)
    expiration_date = timezone.now().date() + timedelta(days=365)

    card = CreditCard.objects.create(
        card_number=card_number,
        expiration_date=expiration_date,
        cvv=cvv,
        account=account,
        card_type='VIRTUAL',
        daily_limit=serializer.validated_data.get('daily_limit', 1000.00),
        monthly_limit=serializer.validated_data.get('monthly_limit', 5000.00)
    )

    return Response(CreditCardSerializer(card).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_card_transactions(request, card_number):
    """
    Récupère l'historique des transactions d'une carte
    """
    try:
        card = CreditCard.objects.get(
            card_number=card_number,
            account__owner=request.user
        )
        transactions = CardTransaction.objects.filter(card=card).order_by('-transaction_date')
        serializer = CardTransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    except CreditCard.DoesNotExist:
        return Response(
            {"error": "Carte introuvable ou non autorisée"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_card_transaction(request):
    """
    Traite une transaction de carte
    """
    try:
        card = CreditCard.objects.get(
            card_number=request.data.get('card_number'),
            account__owner=request.user
        )

        if not card.is_active:
            return Response(
                {"error": "Carte désactivée"},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = float(request.data.get('amount', 0))
        transaction_type = request.data.get('transaction_type', 'PURCHASE')

        # Vérifier les limites
        today_transactions = CardTransaction.objects.filter(
            card=card,
            transaction_date__date=timezone.now().date()
        )
        monthly_transactions = CardTransaction.objects.filter(
            card=card,
            transaction_date__month=timezone.now().month,
            transaction_date__year=timezone.now().year
        )

        if sum(t.amount for t in today_transactions) + amount > card.daily_limit:
            return Response(
                {"error": "Limite quotidienne dépassée"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sum(t.amount for t in monthly_transactions) + amount > card.monthly_limit:
            return Response(
                {"error": "Limite mensuelle dépassée"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Créer la transaction
        transaction = CardTransaction.objects.create(
            card=card,
            amount=amount,
            transaction_type=transaction_type,
            merchant_name=request.data.get('merchant_name'),
            description=request.data.get('description')
        )

        # Mettre à jour le solde du compte
        with transaction.atomic():
            account = card.account
            account.balance -= amount
            account.save()

        return Response(CardTransactionSerializer(transaction).data)

    except CreditCard.DoesNotExist:
        return Response(
            {"error": "Carte introuvable ou non autorisée"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_card_status(request, card_number):
    """
    Active ou désactive une carte
    """
    try:
        card = CreditCard.objects.get(
            card_number=card_number,
            account__owner=request.user
        )
        card.is_active = not card.is_active
        card.save()
        return Response(CreditCardSerializer(card).data)
    except CreditCard.DoesNotExist:
        return Response(
            {"error": "Carte introuvable ou non autorisée"},
            status=status.HTTP_404_NOT_FOUND
        )
