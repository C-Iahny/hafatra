import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Crée un superutilisateur depuis les variables d'environnement (idempotent)"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email    = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        password = os.environ.get('ADMIN_PASSWORD', '')

        if not password:
            self.stdout.write("ADMIN_PASSWORD non défini — commande ignorée.")
            return

        # Supprimer les utilisateurs cassés (email = username au lieu d'une vraie adresse)
        broken = User.objects.filter(email=username)
        if broken.exists():
            broken.delete()
            self.stdout.write(f"Utilisateur cassé supprimé (email='{username}').")

        # Si le bon utilisateur existe déjà, on met juste le mot de passe à jour
        existing = User.objects.filter(username=username).first()
        if existing:
            existing.set_password(password)
            existing.is_superuser = True
            existing.is_staff = True
            existing.save()
            self.stdout.write(f"Superutilisateur '{username}' mis à jour.")
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé."))
        except IntegrityError as e:
            self.stdout.write(f"Erreur création : {e}")
