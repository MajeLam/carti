# 💰 Carti - Simulateur d'API Bancaire avec Django

Carti est un simulateur d'API bancaire développé avec **Django** et **Django REST Framework (DRF)**. Il permet de **créer, gérer et simuler des transactions** entre des comptes bancaires.

---

## 🚀 Fonctionnalités

✔️ Création et gestion des comptes bancaires  
✔️ Récupération du solde d'un compte  
✔️ Transactions (dépôts et retraits)  
✔️ Génération automatique de comptes fictifs  
✔️ Tableau de bord interactif avec statistiques  

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

| Méthode  | Endpoint                            | Description                       |
|----------|------------------------------------|-----------------------------------|
| `GET`    | `/api/accounts/`                   | Liste tous les comptes           |
| `GET`    | `/api/balance/<account_number>/`   | Vérifier le solde d'un compte    |
| `POST`   | `/api/transaction/`                | Effectuer un dépôt ou retrait    |
| `POST`   | `/api/accounts/`                   | Créer un compte bancaire         |

Ajout au solde montant positif ou retrait montant negatif en **cURL** :
```bash
curl -X POST http://127.0.0.1:8000/api/transaction/ \
     -H "Content-Type: application/json" \
     -d '{"account_number": "123456", "amount": 100}'
```
Consulter un solde **cURL** :
```bash
curl -X GET http://127.0.0.1:8000/api/balance/123456/
```
Créer un compte en **cURL** :
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/ \
     -H "Content-Type: application/json" \
     -d '{"account_number": "654321", "owner": "Alice Martin", "balance": 1000, "currency": "USD"}'
```
Faire un virement en **cURL** :
```bash
curl -X POST http://127.0.0.1:8000/api/transfer/ \
     -H "Content-Type: application/json" \
     -d '{"from_account": "123456", "to_account": "654321", "amount": 50}'
```
---

## 🎲 **Génération Automatique de Comptes**
Pour générer des comptes fictifs avec des soldes positifs et négatifs :
```bash
python manage.py create_fake_accounts 10
```
Cela créera **10 comptes aléatoires**.

---

## 🎨 **Interface Web (Tableau de Bord)**
Le projet inclut une interface web accessible à :  
👉 **http://127.0.0.1:8000/**  

Elle affiche :
- 📊 **Nombre de comptes créés**
- ✅ **Comptes positifs / négatifs**
- 💰 **Total des soldes**
- 📋 **Liste des derniers comptes créés**

---

## 🏗️ **Améliorations Possibles**
- 🔐 **Sécurisation avec authentification JWT**
- 📊 **Ajout de graphiques avec Chart.js**
- 🔄 **Transactions entre comptes**
- 📅 **Historique des transactions**

---

## 📜 **Licence**
Ce projet est sous licence **MIT**.  

📩 **Développeur : [Ton Nom]**  
💻 **Contact : [ton-email@example.com]**  
