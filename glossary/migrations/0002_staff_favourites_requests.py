import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("role", models.CharField(blank=True, max_length=120)),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="staff_profiles", to="glossary.organisation"),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="staff_profile", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ["organisation__name", "user__username"]},
        ),
        migrations.CreateModel(
            name="FavouriteSign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "sign",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favourited_by", to="glossary.signentry"),
                ),
                (
                    "staff_profile",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favourites", to="glossary.staffprofile"),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="SignRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("term", models.CharField(max_length=200)),
                ("context", models.TextField(help_text="Where or why this sign is needed.")),
                ("status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected"), ("needs_clarification", "Needs clarification")], default="pending", max_length=30)),
                ("admin_notes", models.TextField(blank=True)),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sign_requests", to="glossary.organisation"),
                ),
                (
                    "requested_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sign_requests", to="glossary.staffprofile"),
                ),
                (
                    "suggested_category",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sign_requests", to="glossary.category"),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="favouritesign",
            constraint=models.UniqueConstraint(fields=("staff_profile", "sign"), name="unique_favourite_sign_per_staff_profile"),
        ),
    ]
