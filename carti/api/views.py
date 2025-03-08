from django.shortcuts import render
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import BankAccount, CreditCard
from .serializers import BankAccountSerializer, CreditCardSerializer




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
def get_balance(request, account_number):
    try:
        account = BankAccount.objects.get(account_number=account_number)
        return Response({"account": account.account_number, "balance": account.balance, "currency": account.currency})
    except BankAccount.DoesNotExist:
        return Response({"error": "Compte introuvable"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def make_transaction(request):
    """
    Effectuer un dépôt ou un retrait
    Expects JSON: {"account_number": "123456", "amount": 100}
    """
    try:
        account = BankAccount.objects.get(account_number=request.data['account_number'])
        amount = (request.data['amount'])

        if amount < 0 and abs(amount) > account.balance:
            return Response({"error": "Fonds insuffisants"}, status=status.HTTP_400_BAD_REQUEST)

        account.balance += amount
        account.save()
        return Response({"message": "Transaction réussie", "new_balance": account.balance})

    except BankAccount.DoesNotExist:
        return Response({"error": "Compte introuvable"}, status=status.HTTP_404_NOT_FOUND)

class BankAccountListCreate(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer

@api_view(['POST'])
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
