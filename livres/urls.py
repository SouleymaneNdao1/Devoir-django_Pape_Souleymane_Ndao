from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.index, name='index'),
    
    # URLs pour les livres
    path('livres/', views.livre_list, name='livre_list'),
    path('livres/nouveau/', views.livre_create, name='livre_create'),
    path('livres/<int:pk>/', views.livre_detail, name='livre_detail'),
    path('livres/<int:pk>/modifier/', views.livre_update, name='livre_update'),
    path('livres/<int:pk>/supprimer/', views.livre_delete, name='livre_delete'),
    
    # URLs pour les emprunts
    path('emprunts/', views.emprunt_list, name='emprunt_list'),
    path('emprunts/nouveau/', views.emprunt_create, name='emprunt_create'),
    path('emprunts/<int:pk>/retour/', views.emprunt_retour, name='emprunt_retour'),
    path('emprunts/<int:pk>/supprimer/', views.emprunt_delete, name='emprunt_delete'),
]
