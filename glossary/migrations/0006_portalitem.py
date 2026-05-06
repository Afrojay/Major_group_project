import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0005_organisation_branding"),
    ]

    operations = [
        migrations.CreateModel(
            name="PortalItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "item_type",
                    models.CharField(
                        choices=[
                            ("task", "Task"),
                            ("appointment", "Appointment"),
                            ("calendar_event", "Calendar event"),
                            ("access_note", "Access note"),
                            ("note", "Note"),
                        ],
                        default="task",
                        max_length=30,
                    ),
                ),
                ("title", models.CharField(max_length=160)),
                ("description", models.TextField(blank=True)),
                ("due_at", models.DateTimeField(blank=True, null=True)),
                ("is_complete", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_portal_items", to="glossary.staffprofile"),
                ),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="portal_items", to="glossary.organisation"),
                ),
            ],
            options={"ordering": ["is_complete", "due_at", "-created_at"]},
        ),
    ]
