import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crée un superutilisateur depuis les variables d'environnement (idempotent)"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('ADMIN_USERNAME', 'Admin')
        email    = os.environ.get('ADMIN_EMAIL', 'miarisoa00@yahoo.de')
        password = os.environ.get('ADMIN_PASSWORD', 'Kanto001!')

        if not password:
            self.stderr.write("ADMIN_PASSWORD non défini — commande ignorée.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Superutilisateur '{username}' existe déjà.")
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur '{username}' créé."))
```

**`Procfile`** → remplace par :
```
web: python manage.py collectstatic --noinput && python manage.py migrate --noinput && python manage.py ensure_admin && daphne -b 0.0.0.0 -p $PORT ZOOT.routing:application