# 💰 Carti - Simulateur d'API Bancaire avec Django

Carti est un simulateur d'API bancaire développé avec **Django** et **Django REST Framework (DRF)**. Il permet de **créer, gérer et simuler des transactions** entre des comptes bancaires.

---

## 🚀 Fonctionnalités

✔️ Création et gestion des comptes bancaires  
✔️ Récupération du solde d'un compte  
✔️ Transactions (dépôts et retraits)  
✔️ Génération automatique de comptes fictifs  
✔️ Tableau de bord interactif avec statistiques  
✔️ Gestion des cartes bancaires (ajout, suppression, liste)  

---

## 🛠️ Installation et Configuration

### 1️⃣ **Cloner le projet**
```bash
git clone https://github.com/ton-repo/carti.git
cd carti
```

### 2️⃣ **Créer un environnement virtuel (optionnel)**
```bash
python -m venv venv
source venv/bin/activate  # Sur Mac/Linux
venv\Scripts\activate      # Sur Windows
```

### 3️⃣ **Installer les dépendances**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Appliquer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

### 6️⃣ **Lancer le serveur**
```bash
python manage.py runserver
```
Accède à l'interface d’administration : **http://127.0.0.1:8000/admin/**  
Accède au tableau de bord : **http://127.0.0.1:8000/**  

---

## 🔗 **Endpoints de l'API**

| Méthode  | Endpoint                                         | Description                                    |
|----------|--------------------------------------------------|------------------------------------------------|
| `GET`    | `/api/accounts/`                                  | Liste tous les comptes                         |
| `GET`    | `/api/balance/<account_number>/`                   | Vérifier le solde d'un compte                   |
| `POST`   | `/api/transaction/`                                | Effectuer un dépôt ou retrait                  |
| `POST`   | `/api/accounts/`                                   | Créer un compte bancaire                       |
| `GET`    | `/api/cards/<account_number>/`                     | Lister les cartes d'un compte                  |
| `POST`   | `/api/add-card/`                                   | Ajouter une carte bancaire                    |
| `DELETE` | `/api/delete-card/<card_number>/`                  | Supprimer une carte bancaire                  |
| `POST`   | `/api/transfer/`                                   | Effectuer un virement entre comptes           |

---

## 💳 **Gestion des Cartes Bancaires**

### 📌 **Exemples d'utilisation en `cURL`**

#### ✅ **1. Lister les cartes d’un compte**
```bash
curl -X GET http://127.0.0.1:8000/api/cards/123456/
```

#### ✅ **2. Ajouter une carte à un compte**
```bash
curl -X POST http://127.0.0.1:8000/api/add-card/      -H "Content-Type: application/json"      -d '{
            "card_number": "1234567890123456",
            "expiration_date": "2026-12-31",
            "cvv": "123",
            "account": 1
         }'
```

#### ❌ **3. Supprimer une carte**
```bash
curl -X DELETE http://127.0.0.1:8000/api/delete-card/1234567890123456/
```

---

## 🔒 **Sécurité et Améliorations**

- 🔐 **Masquer les CVV** dans les réponses pour plus de sécurité.  
- 🛡️ **Ajouter une authentification** (par exemple JWT) pour sécuriser l'accès aux endpoints.  
- 📅 **Gérer l'expiration** des cartes automatiquement.  

---

## 🎲 **Génération Automatique de Comptes**
Pour générer des comptes fictifs avec des soldes positifs et négatifs :
```bash
python manage.py create_fake_accounts 10
```
Cela créera **10 comptes aléatoires**.

---

## 🏗️ **Améliorations Possibles**

- 📊 **Tableau de bord amélioré** avec un historique des transactions par carte.  
- 📅 **Rappels pour les expirations** de cartes bancaires.  
- 🔄 **Système de transfert inter-comptes** optimisé.  

---

## 📜 **Licence**
Ce projet est sous licence **MIT**.  

📩 **Développeur : [Ton Nom]**  
💻 **Contact : [ton-email@example.com]**  
