import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q


class Command(BaseCommand):
    help = "Crée un superutilisateur depuis les variables d'environnement (idempotent)"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email    = os.environ.get('ADMIN_EMAIL', 'miarisoa00@yahoo.de')
        password = os.environ.get('ADMIN_PASSWORD', '')

        if not password:
            self.stdout.write("ADMIN_PASSWORD non défini — commande ignorée.")
            return

        # Supprimer tous les utilisateurs avec un email invalide (sans '@')
        broken_qs = User.objects.filter(~Q(email__contains='@'))
        count = broken_qs.count()
        if count:
            broken_qs.delete()
            self.stdout.write(f"Nettoyage : {count} utilisateur(s) cassé(s) supprimé(s).")

        # Si l'admin existe déjà (par email), on met à jour le mot de passe
        existing = User.objects.filter(email=email).first()
        if existing:
            existing.set_password(password)
            existing.is_superuser = True
            existing.is_staff = True
            existing.is_admin = True
            existing.save()
            self.stdout.write(f"Superutilisateur '{existing.username}' mis à jour.")
            return

        try:
            User.objects.create_superuser(email=email, username=username, password=password)
            self.stdout.write(self.style.SUCCESS(
                f"Superutilisateur '{username}' ({email}) créé."
            ))
        except IntegrityError as e:
            self.stdout.write(f"Erreur : {e}")
