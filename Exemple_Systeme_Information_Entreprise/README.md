# Exemple de système d'information — Python Backend + Frontend

Auteur : **Pr . SEBRI Abderrahim ** 

Projet pédagogique simple de gestion des employés, avec :
- **Backend** : Python + FastAPI
- **Base de données** : SQLite
- **Frontend** : HTML, CSS et JavaScript
- **API REST** : opérations CRUD (lister, consulter, créer, modifier, supprimer)

## Prérequis
- Python 3.10 ou plus récent
- pip

## Installation
Dans un terminal, placez-vous dans le dossier du projet puis exécutez :

```bash
python -m venv .venv
```

Activation de l'environnement :
- Windows : `.venv\Scripts\activate`
- Linux/macOS : `source .venv/bin/activate`

Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement
Depuis la racine du projet :

```bash
uvicorn backend.main:app --reload
```

Ouvrez ensuite :
- Interface utilisateur : http://127.0.0.1:8000
- Documentation interactive de l'API : http://127.0.0.1:8000/docs

La base SQLite `employees.db` est créée automatiquement au premier lancement.

## Structure
```text
exemple_systeme_information/
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── requirements.txt
└── README.md
```

## Endpoints principaux
- `GET /api/employees` : liste des employés
- `GET /api/employees/{id}` : détail d'un employé
- `POST /api/employees` : création
- `PUT /api/employees/{id}` : modification
- `DELETE /api/employees/{id}` : suppression

## Limites et sécurité
Ce projet est une **base de démonstration**, pas une application prête pour la production.
Avant une mise en production, ajouter notamment l'authentification et les autorisations, des migrations de base de données, des tests automatisés, une validation renforcée, une journalisation, une configuration par variables d'environnement, des sauvegardes et une protection adaptée contre les abus.
