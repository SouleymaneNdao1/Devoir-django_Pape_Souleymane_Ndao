from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Count, Case, When, IntegerField
from .models import Livre, Emprunt
from datetime import date


def index(request):
    """Page d'accueil avec statistiques"""
    total_livres = Livre.objects.count()
    livres_disponibles = Livre.objects.filter(
        Q(emprunts__isnull=True) | Q(emprunts__date_retour__isnull=False)
    ).distinct().count()
    
    emprunts_en_cours = Emprunt.objects.filter(date_retour__isnull=True).count()
    
    context = {
        'total_livres': total_livres,
        'livres_disponibles': livres_disponibles,
        'emprunts_en_cours': emprunts_en_cours,
    }
    return render(request, 'livres/index.html', context)


def livre_list(request):
    """Liste des livres avec pagination et recherche"""
    query = request.GET.get('q', '')
    
    livres = Livre.objects.all()
    
    # Recherche
    if query:
        livres = livres.filter(
            Q(titre__icontains=query) |
            Q(auteur__icontains=query) |
            Q(isbn__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(livres, 10)  # 10 livres par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'livres/livre_list.html', context)


def livre_detail(request, pk):
    """Détails d'un livre avec historique des emprunts"""
    livre = get_object_or_404(Livre, pk=pk)
    emprunts = livre.emprunts.all()[:10]  # 10 derniers emprunts
    
    context = {
        'livre': livre,
        'emprunts': emprunts,
    }
    return render(request, 'livres/livre_detail.html', context)


def livre_create(request):
    """Créer un nouveau livre"""
    if request.method == 'POST':
        titre = request.POST.get('titre')
        auteur = request.POST.get('auteur')
        isbn = request.POST.get('isbn')
        
        if titre and auteur and isbn:
            try:
                livre = Livre.objects.create(
                    titre=titre,
                    auteur=auteur,
                    isbn=isbn
                )
                messages.success(request, f'Le livre "{livre.titre}" a été ajouté avec succès.')
                return redirect('livre_detail', pk=livre.pk)
            except Exception as e:
                messages.error(request, f'Erreur : {str(e)}')
        else:
            messages.error(request, 'Tous les champs sont obligatoires.')
    
    return render(request, 'livres/livre_form.html')


def livre_update(request, pk):
    """Modifier un livre"""
    livre = get_object_or_404(Livre, pk=pk)
    
    if request.method == 'POST':
        livre.titre = request.POST.get('titre')
        livre.auteur = request.POST.get('auteur')
        livre.isbn = request.POST.get('isbn')
        
        try:
            livre.save()
            messages.success(request, f'Le livre "{livre.titre}" a été modifié avec succès.')
            return redirect('livre_detail', pk=livre.pk)
        except Exception as e:
            messages.error(request, f'Erreur : {str(e)}')
    
    context = {'livre': livre}
    return render(request, 'livres/livre_form.html', context)


def livre_delete(request, pk):
    """Supprimer un livre"""
    livre = get_object_or_404(Livre, pk=pk)
    
    if request.method == 'POST':
        titre = livre.titre
        livre.delete()
        messages.success(request, f'Le livre "{titre}" a été supprimé avec succès.')
        return redirect('livre_list')
    
    context = {'livre': livre}
    return render(request, 'livres/livre_confirm_delete.html', context)


def emprunt_list(request):
    """Liste des emprunts avec pagination"""
    filter_type = request.GET.get('filter', 'all')
    
    emprunts = Emprunt.objects.select_related('livre').all()
    
    # Filtres
    if filter_type == 'en_cours':
        emprunts = emprunts.filter(date_retour__isnull=True)
    elif filter_type == 'retournes':
        emprunts = emprunts.filter(date_retour__isnull=False)
    
    # Pagination
    paginator = Paginator(emprunts, 15)  # 15 emprunts par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_type': filter_type,
    }
    return render(request, 'livres/emprunt_list.html', context)


def emprunt_create(request):
    """Créer un nouvel emprunt"""
    if request.method == 'POST':
        livre_id = request.POST.get('livre')
        date_emprunt = request.POST.get('date_emprunt')
        
        if livre_id and date_emprunt:
            livre = get_object_or_404(Livre, pk=livre_id)
            
            # Vérifier si le livre est disponible
            if not livre.est_disponible():
                messages.error(request, f'Le livre "{livre.titre}" est déjà emprunté.')
            else:
                emprunt = Emprunt.objects.create(
                    livre=livre,
                    date_emprunt=date_emprunt
                )
                messages.success(request, f'Emprunt du livre "{livre.titre}" enregistré avec succès.')
                return redirect('emprunt_list')
        else:
            messages.error(request, 'Tous les champs sont obligatoires.')
    
    livres_disponibles = Livre.objects.all()
    context = {
        'livres': livres_disponibles,
        'today': date.today().isoformat(),
    }
    return render(request, 'livres/emprunt_form.html', context)


def emprunt_retour(request, pk):
    """Enregistrer le retour d'un emprunt"""
    emprunt = get_object_or_404(Emprunt, pk=pk)
    
    if request.method == 'POST':
        date_retour = request.POST.get('date_retour')
        
        if date_retour:
            emprunt.date_retour = date_retour
            emprunt.save()
            messages.success(request, f'Retour du livre "{emprunt.livre.titre}" enregistré avec succès.')
            return redirect('emprunt_list')
        else:
            messages.error(request, 'La date de retour est obligatoire.')
    
    context = {
        'emprunt': emprunt,
        'today': date.today().isoformat(),
    }
    return render(request, 'livres/emprunt_retour.html', context)


def emprunt_delete(request, pk):
    """Supprimer un emprunt"""
    emprunt = get_object_or_404(Emprunt, pk=pk)
    
    if request.method == 'POST':
        livre_titre = emprunt.livre.titre
        emprunt.delete()
        messages.success(request, f'L\'emprunt du livre "{livre_titre}" a été supprimé.')
        return redirect('emprunt_list')
    
    context = {'emprunt': emprunt}
    return render(request, 'livres/emprunt_confirm_delete.html', context)
