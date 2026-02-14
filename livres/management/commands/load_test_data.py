from django.core.management.base import BaseCommand
from livres.models import Livre, Emprunt
from datetime import datetime, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Charge des données de test dans la base de données'

    def handle(self, *args, **kwargs):
        self.stdout.write('Chargement des données de test...')

        # Supprimer les données existantes (optionnel)
        Emprunt.objects.all().delete()
        Livre.objects.all().delete()

        # Créer des livres
        livres_data = [
            {'titre': '1984', 'auteur': 'George Orwell', 'isbn': '9780451524935'},
            {'titre': 'Le Petit Prince', 'auteur': 'Antoine de Saint-Exupéry', 'isbn': '9782070612758'},
            {'titre': 'Harry Potter à l\'école des sorciers', 'auteur': 'J.K. Rowling', 'isbn': '9782070584628'},
            {'titre': 'L\'Étranger', 'auteur': 'Albert Camus', 'isbn': '9782070360024'},
            {'titre': 'Les Misérables', 'auteur': 'Victor Hugo', 'isbn': '9782253096337'},
            {'titre': 'Le Seigneur des Anneaux', 'auteur': 'J.R.R. Tolkien', 'isbn': '9782266154345'},
            {'titre': 'Crime et Châtiment', 'auteur': 'Fiodor Dostoïevski', 'isbn': '9782253085768'},
            {'titre': 'Cent ans de solitude', 'auteur': 'Gabriel García Márquez', 'isbn': '9782020238113'},
            {'titre': 'L\'Alchimiste', 'auteur': 'Paulo Coelho', 'isbn': '9782290349960'},
            {'titre': 'Orgueil et Préjugés', 'auteur': 'Jane Austen', 'isbn': '9782290315033'},
            {'titre': 'La Peste', 'auteur': 'Albert Camus', 'isbn': '9782070360420'},
            {'titre': 'Voyage au bout de la nuit', 'auteur': 'Louis-Ferdinand Céline', 'isbn': '9782070360178'},
            {'titre': 'Les Fleurs du mal', 'auteur': 'Charles Baudelaire', 'isbn': '9782253082156'},
            {'titre': 'Madame Bovary', 'auteur': 'Gustave Flaubert', 'isbn': '9782253004714'},
            {'titre': 'Le Comte de Monte-Cristo', 'auteur': 'Alexandre Dumas', 'isbn': '9782253098058'},
        ]

        livres = []
        for livre_data in livres_data:
            livre = Livre.objects.create(**livre_data)
            livres.append(livre)
            self.stdout.write(self.style.SUCCESS(f'✓ Livre créé : {livre.titre}'))

        # Créer des emprunts (certains en cours, d'autres retournés)
        today = timezone.now().date()
        
        emprunts_data = [
            # Emprunts en cours
            {'livre': livres[0], 'date_emprunt': today - timedelta(days=5), 'date_retour': None},
            {'livre': livres[2], 'date_emprunt': today - timedelta(days=10), 'date_retour': None},
            {'livre': livres[5], 'date_emprunt': today - timedelta(days=3), 'date_retour': None},
            
            # Emprunts retournés
            {'livre': livres[1], 'date_emprunt': today - timedelta(days=30), 'date_retour': today - timedelta(days=15)},
            {'livre': livres[3], 'date_emprunt': today - timedelta(days=45), 'date_retour': today - timedelta(days=32)},
            {'livre': livres[4], 'date_emprunt': today - timedelta(days=60), 'date_retour': today - timedelta(days=48)},
            {'livre': livres[1], 'date_emprunt': today - timedelta(days=90), 'date_retour': today - timedelta(days=75)},
            {'livre': livres[6], 'date_emprunt': today - timedelta(days=20), 'date_retour': today - timedelta(days=8)},
            {'livre': livres[7], 'date_emprunt': today - timedelta(days=25), 'date_retour': today - timedelta(days=12)},
            {'livre': livres[8], 'date_emprunt': today - timedelta(days=35), 'date_retour': today - timedelta(days=21)},
        ]

        for emprunt_data in emprunts_data:
            emprunt = Emprunt.objects.create(**emprunt_data)
            status = "en cours" if emprunt.est_en_cours() else "retourné"
            self.stdout.write(self.style.SUCCESS(f'✓ Emprunt créé : {emprunt.livre.titre} ({status})'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Chargement terminé !'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(livres)} livres créés'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(emprunts_data)} emprunts créés'))
        
        # Statistiques
        livres_disponibles = sum(1 for livre in livres if livre.est_disponible())
        self.stdout.write(self.style.SUCCESS(f'  - {livres_disponibles} livres disponibles'))
        self.stdout.write(self.style.SUCCESS(f'  - {len(livres) - livres_disponibles} livres empruntés'))
