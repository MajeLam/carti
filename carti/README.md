# Carti - API de Gestion Bancaire

## Description
Carti est une API REST pour la gestion de comptes bancaires, cartes de crédit et transactions.

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd carti
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
.\venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations
```bash
python manage.py migrate
```

5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

6. Lancer le serveur
```bash
python manage.py runserver
```

## API Endpoints

### Authentification

#### Inscription
```http
POST /api/auth/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "phone_number": "+33612345678",
    "address": "123 rue Example",
    "date_of_birth": "1990-01-01"
}
```

#### Connexion
```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

Réponse :
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Comptes Bancaires

#### Lister ses comptes
```http
GET /api/accounts/
Authorization: Bearer <token>
```

Réponse :
```json
[
    {
        "id": 1,
        "account_number": "1234567890",
        "owner": {
            "id": 1,
            "username": "user",
            "email": "user@example.com",
            "phone_number": "+33612345678",
            "address": "123 rue Example",
            "date_of_birth": "1990-01-01"
        },
        "balance": 1000.00,
        "currency": "EUR",
        "created_at": "2024-03-14T10:00:00Z",
        "updated_at": "2024-03-14T10:00:00Z"
    }
]
```

#### Créer un compte
```http
POST /api/accounts/
Authorization: Bearer <token>
Content-Type: application/json

{
    "currency": "EUR",
    "initial_balance": 1000.00
}
```

#### Consulter le solde d'un compte
```http
GET /api/balance/1234567890/
Authorization: Bearer <token>
```

Réponse :
```json
{
    "account": "1234567890",
    "balance": 1000.00,
    "currency": "EUR"
}
```

#### Effectuer une transaction
```http
POST /api/transaction/
Authorization: Bearer <token>
Content-Type: application/json

{
    "account_number": "1234567890",
    "amount": 100.00  # Montant positif pour un dépôt, négatif pour un retrait
}
```

Réponse :
```json
{
    "message": "Transaction réussie",
    "new_balance": 1100.00
}
```

#### Effectuer un virement
```http
POST /api/transfer/
Authorization: Bearer <token>
Content-Type: application/json

{
    "from_account": "1234567890",
    "to_account": "0987654321",
    "amount": 50.00
}
```

Réponse :
```json
{
    "message": "Virement réussi",
    "from_account": "1234567890",
    "to_account": "0987654321",
    "transferred_amount": 50.00,
    "new_balance_from": 950.00,
    "new_balance_to": 1050.00
}
```

### Cartes Bancaires

#### Lister les cartes d'un compte
```http
GET /api/cards/1234567890/
Authorization: Bearer <token>
```

#### Créer une carte virtuelle
```http
POST /api/virtual-cards/
Authorization: Bearer <token>
Content-Type: application/json

{
    "account_number": "1234567890",
    "daily_limit": 1000.00,
    "monthly_limit": 5000.00
}
```

#### Effectuer une transaction par carte
```http
POST /api/cards/transaction/
Authorization: Bearer <token>
Content-Type: application/json

{
    "card_number": "1234567890123456",
    "amount": 50.00,
    "transaction_type": "PURCHASE",
    "merchant_name": "Super Marché",
    "description": "Courses"
}
```

## Sécurité

- Toutes les requêtes API nécessitent une authentification via JWT
- Chaque utilisateur ne peut accéder qu'à ses propres comptes
- Les transactions ne sont possibles que sur les comptes appartenant à l'utilisateur connecté
- Les virements ne sont possibles qu'à partir de comptes appartenant à l'utilisateur connecté

## Exemples d'utilisation avec curl

### Connexion
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Lister les comptes
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/accounts/
```

### Consulter un solde
```bash
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/balance/1234567890/
```

### Effectuer une transaction
```bash
curl -X POST http://localhost:8000/api/transaction/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "1234567890",
    "amount": 100.00
  }'
```

## Modèles de Données

### User
- email (unique)
- username
- password
- phone_number
- address
- date_of_birth
- created_at
- updated_at

### BankAccount
- account_number (unique)
- owner (ForeignKey -> User)
- balance
- currency
- created_at
- updated_at

### CreditCard
- card_number (unique)
- expiration_date
- cvv
- account (ForeignKey -> BankAccount)
- card_type (PHYSICAL/VIRTUAL)
- is_active
- daily_limit
- monthly_limit
- created_at
- updated_at

### CardTransaction
- card (ForeignKey -> CreditCard)
- amount
- transaction_type (PURCHASE/WITHDRAWAL/TRANSFER)
- merchant_name
- transaction_date
- status
- description

## Gestion des Erreurs

Les erreurs sont renvoyées au format suivant :
```json
{
    "error": "Description de l'erreur",
    "code": "CODE_ERREUR",
    "details": {
        "champ": ["Message d'erreur spécifique"]
    }
}
```

Codes d'erreur courants :
- 400 : Requête invalide
- 401 : Non authentifié
- 403 : Non autorisé
- 404 : Ressource non trouvée
- 429 : Trop de requêtes
- 500 : Erreur serveur

## Tests

Pour exécuter les tests :
```bash
python manage.py test
```

## Déploiement

1. Configurer les variables d'environnement
2. Désactiver le mode DEBUG
3. Configurer un serveur WSGI (Gunicorn)
4. Configurer un serveur web (Nginx)
5. Configurer SSL/TLS
6. Configurer la base de données de production 