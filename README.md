# Système de Gestion de Bibliothèque - Django

Un système CRUD complet et moderne pour gérer une bibliothèque avec des livres et des emprunts.

##  Fonctionnalités

### Gestion des Livres
-  Créer, lire, modifier et supprimer des livres
-  Recherche par titre, auteur ou ISBN
-  Affichage du statut (disponible/emprunté)
-  Historique complet des emprunts par livre
-  Pagination (10 livres par page)

### Gestion des Emprunts
-  Enregistrer de nouveaux emprunts
-  Marquer les retours de livres
-  Filtrer les emprunts (tous/en cours/retournés)
-  Supprimer des emprunts
-  Pagination (15 emprunts par page)
-  Validation : emprunts uniquement pour livres disponibles

### Tableau de Bord
-  Statistiques en temps réel :
  - Nombre total de livres
  - Nombre de livres disponibles
  - Nombre d'emprunts en cours

### Design
-  Interface moderne avec esthétique éditoriale
-  Typographie distinctive (Crimson Pro + Work Sans)
-  Palette de couleurs terre chaude
-  Animations et transitions fluides
-  Responsive design
-  Messages de confirmation/erreur

##  Installation

### Prérequis
- Python 3.8+
- Django 4.2+

### Étapes d'installation

1. **Cloner ou télécharger le projet**
```bash
cd devoir django_Pape_Souleymane_Ndao
```

2. **Installer Django** (si nécessaire)
```bash
pip install django
```

3. **Effectuer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Créer un superutilisateur** (optionnel, pour accéder à l'admin Django)
```bash
python manage.py createsuperuser
```

5. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

6. **Accéder à l'application**
- Application : http://127.0.0.1:8000/
- Admin Django : http://127.0.0.1:8000/admin/

##  Structure du Projet

```
bibliotheque_projet/
│
├── bibliotheque/              # Configuration du projet
│   ├── __init__.py
│   ├── settings.py           # Paramètres Django
│   ├── urls.py               # URLs principales
│   └── wsgi.py
│
├── livres/                    # Application principale
│   ├── migrations/           # Migrations de base de données
│   ├── static/
│   │   └── css/
│   │       └── style.css     # Styles CSS modernes
│   ├── templates/
│   │   └── livres/          # Templates HTML
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── livre_list.html
│   │       ├── livre_detail.html
│   │       ├── livre_form.html
│   │       ├── livre_confirm_delete.html
│   │       ├── emprunt_list.html
│   │       ├── emprunt_form.html
│   │       ├── emprunt_retour.html
│   │       └── emprunt_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py             # Configuration admin Django
│   ├── apps.py
│   ├── models.py            # Modèles Livre et Emprunt
│   ├── urls.py              # URLs de l'application
│   └── views.py             # Vues et logique métier
│
├── db.sqlite3               # Base de données SQLite
└── manage.py                # Script de gestion Django
```

##  Modèles de Données

### Livre
- `id` : Identifiant unique (auto-généré)
- `titre` : Titre du livre (CharField)
- `auteur` : Nom de l'auteur (CharField)
- `isbn` : Numéro ISBN à 13 chiffres (CharField, unique)
- `created_at` : Date de création
- `updated_at` : Date de modification

**Méthodes :**
- `est_disponible()` : Vérifie si le livre est disponible
- `nombre_emprunts()` : Retourne le nombre d'emprunts

### Emprunt
- `id` : Identifiant unique (auto-généré)
- `livre` : Référence au livre emprunté (ForeignKey)
- `date_emprunt` : Date de l'emprunt
- `date_retour` : Date de retour (nullable)
- `created_at` : Date de création
- `updated_at` : Date de modification

**Méthodes :**
- `est_en_cours()` : Vérifie si l'emprunt est en cours

##  Caractéristiques du Design

### Typographie
- **Titres** : Crimson Pro (serif, élégante)
- **Texte** : Work Sans (sans-serif, moderne)

### Palette de Couleurs
- **Primary** : `#2C1810` (brun foncé)
- **Secondary** : `#8B4513` (saddle brown)
- **Accent** : `#D4691A` (chocolate)
- **Background** : `#FAF8F5` (blanc cassé)
- **Success** : `#2D5F3F` (vert forêt)
- **Warning** : `#C87941` (orange terre)
- **Danger** : `#A4372A` (rouge brique)

### Animations
- Transitions fluides sur les cartes et boutons
- Effet de hover avec élévation
- Messages animés avec slide-in
- Animations de chargement subtiles

##  Utilisation

### Ajouter un livre
1. Cliquer sur "Ajouter un livre" depuis la page d'accueil ou la liste
2. Remplir le formulaire (titre, auteur, ISBN)
3. Cliquer sur "Ajouter le livre"

### Emprunter un livre
1. Aller sur "Emprunts" → "Nouvel emprunt"
2. Sélectionner un livre disponible
3. Choisir la date d'emprunt
4. Cliquer sur "Enregistrer l'emprunt"

### Retourner un livre
1. Dans la liste des emprunts, cliquer sur "Retourner"
2. Sélectionner la date de retour
3. Cliquer sur "Confirmer le retour"

### Rechercher un livre
1. Utiliser la barre de recherche sur la page "Livres"
2. Taper le titre, auteur ou ISBN
3. Les résultats s'affichent avec pagination

##  Personnalisation

### Modifier la pagination
Dans `livres/views.py`, changez le nombre d'éléments par page :
```python
# Pour les livres
paginator = Paginator(livres, 10)  # Modifier le 10

# Pour les emprunts
paginator = Paginator(emprunts, 15)  # Modifier le 15
```

### Modifier les couleurs
Dans `livres/static/css/style.css`, modifiez les variables CSS :
```css
:root {
    --color-primary: #2C1810;
    --color-accent: #D4691A;
    /* etc... */
}
```

##  Administration Django

Accédez à l'interface d'administration Django pour une gestion avancée :

1. Créez un superutilisateur : `python manage.py createsuperuser`
2. Accédez à http://127.0.0.1:8000/admin/
3. Connectez-vous avec vos identifiants

L'admin offre des fonctionnalités supplémentaires :
- Filtres avancés
- Recherche puissante
- Export de données
- Gestion en masse

##  Validation des Données

### Livre
- **Titre** : Obligatoire, max 200 caractères
- **Auteur** : Obligatoire, max 200 caractères
- **ISBN** : Obligatoire, exactement 13 chiffres, unique

### Emprunt
- **Livre** : Doit être disponible (non emprunté)
- **Date d'emprunt** : Obligatoire
- **Date de retour** : Doit être >= date d'emprunt (si fournie)

##  Technologies Utilisées

- **Backend** : Django 4.2+
- **Frontend** : HTML5, CSS3 (avec variables CSS)
- **Base de données** : SQLite
- **Typographie** : Google Fonts (Crimson Pro, Work Sans)
- **Architecture** : MVC (Model-View-Controller)

