from django.contrib import admin
from .models import Categorie
from .models import Article

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom',)  
    search_fields = ('nom',) 


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'categorie', 'date_publication', 'image')
    list_filter = ('categorie', 'date_publication')
    search_fields = ('titre', 'contenu')

    fieldsets = (
        ('Informations principales', {'fields': ('titre', 'contenu', 'image')}),  # ajouter image ici
        ('Classification', {'fields': ('categorie', 'auteur')}),
    )
