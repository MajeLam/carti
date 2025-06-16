from django.urls import path
from .views import get_balance, make_transaction, BankAccountListCreate, home, transfer_funds, list_cards, add_card, delete_card, create_virtual_card, get_card_transactions, process_card_transaction, toggle_card_status, login_view, register_view

urlpatterns = [
    path('', home, name="home"),
    
    # Authentication
    path('auth/login/', login_view, name="login"),
    path('auth/register/', register_view, name="register"),
    
    # Accounts
    path('accounts/', BankAccountListCreate.as_view(), name="account-list"),
    path('balance/<str:account_number>/', get_balance, name="get-balance"),
    path('transaction/', make_transaction, name="make-transaction"),
    path('transfer/', transfer_funds, name="transfer-funds"),

    # Cards
    path('cards/<str:account_number>/', list_cards, name="list-cards"),
    path('add-card/', add_card, name="add-card"),
    path('delete-card/<str:card_number>/', delete_card, name="delete-card"),
    path('virtual-cards/', create_virtual_card, name='create-virtual-card'),
    path('cards/<str:card_number>/transactions/', get_card_transactions, name='card-transactions'),
    path('cards/transaction/', process_card_transaction, name='process-transaction'),
    path('cards/<str:card_number>/toggle/', toggle_card_status, name='toggle-card-status'),
]
