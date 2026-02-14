from django.db import models
from django.utils import timezone


class Livre(models.Model):
    titre = models.CharField(max_length=200, verbose_name="Titre")
    auteur = models.CharField(max_length=200, verbose_name="Auteur")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Livre"
        verbose_name_plural = "Livres"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titre} - {self.auteur}"

    def est_disponible(self):
        """Vérifie si le livre est actuellement disponible (non emprunté ou retourné)"""
        derniers_emprunts = self.emprunts.filter(
            date_retour__isnull=True
        ).exists()
        return not derniers_emprunts

    def nombre_emprunts(self):
        """Retourne le nombre total d'emprunts pour ce livre"""
        return self.emprunts.count()


class Emprunt(models.Model):
    livre = models.ForeignKey(
        Livre, 
        on_delete=models.CASCADE, 
        related_name='emprunts',
        verbose_name="Livre"
    )
    date_emprunt = models.DateField(
        default=timezone.now,
        verbose_name="Date d'emprunt"
    )
    date_retour = models.DateField(
        null=True, 
        blank=True,
        verbose_name="Date de retour"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Emprunt"
        verbose_name_plural = "Emprunts"
        ordering = ['-date_emprunt']

    def __str__(self):
        status = "En cours" if not self.date_retour else f"Retourné le {self.date_retour}"
        return f"{self.livre.titre} - {status}"

    def est_en_cours(self):
        """Vérifie si l'emprunt est toujours en cours"""
        return self.date_retour is None
