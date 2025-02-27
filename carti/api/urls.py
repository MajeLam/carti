from django.urls import path
from .views import get_balance, make_transaction, BankAccountListCreate, home

urlpatterns = [
    path('', home, name="home"),
    path('accounts/', BankAccountListCreate.as_view(), name="account-list"),
    path('balance/<str:account_number>/', get_balance, name="get-balance"),
    path('transaction/', make_transaction, name="make-transaction"),
]
