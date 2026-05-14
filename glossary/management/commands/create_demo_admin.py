import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update a demo superuser from environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("DEMO_ADMIN_USERNAME")
        password = os.environ.get("DEMO_ADMIN_PASSWORD")
        email = os.environ.get("DEMO_ADMIN_EMAIL", "")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "DEMO_ADMIN_USERNAME or DEMO_ADMIN_PASSWORD is not set. Skipping admin creation."
                )
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Demo admin {username} {action}."))
