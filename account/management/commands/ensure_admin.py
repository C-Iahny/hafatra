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

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superutilisateur '{username}' existe déjà.")
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(f"Email '{email}' déjà utilisé — supprime l'utilisateur cassé en base d'abord.")
            return

        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé."))
        except IntegrityError as e:
            self.stdout.write(f"Erreur : {e}")
