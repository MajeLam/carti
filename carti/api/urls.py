from django.urls import path
from .views import get_balance, make_transaction, BankAccountListCreate, home, transfer_funds, list_cards, add_card, delete_card

urlpatterns = [
    path('', home, name="home"),
    
    path('accounts/', BankAccountListCreate.as_view(), name="account-list"),
    path('balance/<str:account_number>/', get_balance, name="get-balance"),
    path('transaction/', make_transaction, name="make-transaction"),
    path('transfer/', transfer_funds, name="transfer-funds"),

    path('cards/<str:account_number>/', list_cards, name="list-cards"),
    path('add-card/', add_card, name="add-card"),
    path('delete-card/<str:card_number>/', delete_card, name="delete-card"),
]
