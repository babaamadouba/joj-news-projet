from django.db import models
from django.contrib.auth.models import User

# =======================
# Modèle Catégorie
# =======================
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # facultatif

    def __str__(self):
        return self.nom


# =======================
# Modèle Article
# =======================
class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, related_name='articles')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(auto_now_add=True)
    
    # === nouveau champ image ===
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    def __str__(self):
        return self.titre

    def extrait(self, n=100):
        if len(self.contenu) > n:
            return self.contenu[:n] + "..."
        return self.contenu

# =======================
# Modèle Commentaire
# =======================
class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur.username} - {self.article.titre}"