from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import BankAccount
from .serializers import BankAccountSerializer

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