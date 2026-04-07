from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Commentaire

@receiver(post_save, sender=Commentaire)
def notifier_admin_nouveau_commentaire(sender, instance, created, **kwargs):
    if created:
        # Titre de l'article lié
        titre_article = instance.article.titre
        auteur = instance.auteur.username
        contenu_commentaire = instance.contenu

        # Email à l'admin (dans dev, affiché en console)
        send_mail(
            subject=f"Nouveau commentaire sur '{titre_article}'",
            message=f"Le commentaire suivant a été ajouté par {auteur} :\n\n{contenu_commentaire}",
            from_email='webmaster@jojnews.com',
            recipient_list=['admin@jojnews.com'],  # peut être n'importe quelle adresse
        )