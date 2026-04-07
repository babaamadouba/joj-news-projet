from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.urls import path
from . import views
from .views import ArticleDetailView 
from .views import ModifierCommentaire, SupprimerCommentaire



urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='detail_article'),  # <- as_view() obligatoire
    path('commentaire/<int:pk>/modifier/', ModifierCommentaire.as_view(), name='modifier_commentaire'),
    path('commentaire/<int:pk>/supprimer/', SupprimerCommentaire.as_view(), name='supprimer_commentaire'),

]

