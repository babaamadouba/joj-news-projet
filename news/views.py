from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import DetailView
from .models import Article, Commentaire
from .forms import InscriptionForm, CommentaireForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth import logout
# =======================
# Inscription
# =======================
def inscription_view(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # utilisateur normal
            user.save()
            login(request, user)  # connexion automatique
            messages.success(request, "Inscription réussie !")
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})


# =======================
# Connexion
# =======================
def connexion_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('accueil')  # redirige vers la vue accueil
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    return render(request, 'connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')  # ou 'accueil'


# =======================
# Accueil
# =======================
def accueil_view(request):
    articles = Article.objects.select_related('categorie', 'auteur').order_by('-date_publication')
    return render(request, 'acceuil.html', {'articles': articles})


# =======================
# Détail Article / Commentaires
# =======================
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Seulement si l'utilisateur est connecté, on crée le formulaire
        if self.request.user.is_authenticated:
            context['form'] = CommentaireForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour commenter.")
            return redirect('connexion')

        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = self.object
            commentaire.auteur = request.user
            commentaire.save()
            messages.success(request, "Commentaire ajouté avec succès !")
        else:
            messages.error(request, "Erreur lors de l'ajout du commentaire.")

        return redirect('detail_article', pk=self.object.pk)
    
class ModifierCommentaire(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
     model = Commentaire
     fields = ['contenu']
     template_name = 'modifier_commentaire.html'

     def get_success_url(self):
        return reverse_lazy('detail_article', kwargs={'pk': self.object.article.pk})

     def test_func(self):
        commentaire = self.get_object()
        return self.request.user == commentaire.auteur
     


class SupprimerCommentaire(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Commentaire
    template_name = 'supprimer_commentaire.html'

    def get_success_url(self):
        return reverse_lazy('detail_article', kwargs={'pk': self.object.article.pk})

    def test_func(self):
        commentaire = self.get_object()
        return self.request.user == commentaire.auteur