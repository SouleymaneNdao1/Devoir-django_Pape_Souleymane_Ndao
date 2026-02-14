from django.contrib import admin
from .models import Livre, Emprunt


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'isbn', 'est_disponible', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('titre', 'auteur', 'isbn')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('livre', 'date_emprunt', 'date_retour', 'est_en_cours')
    list_filter = ('date_emprunt', 'date_retour')
    search_fields = ('livre__titre', 'livre__auteur')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_emprunt'
