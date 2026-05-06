import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Organisation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True)),
                ("contact_email", models.EmailField(blank=True, max_length=254)),
                ("theme_colour", models.CharField(default="#2563eb", max_length=20)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField()),
                ("description", models.TextField(blank=True)),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="categories", to="glossary.organisation"),
                ),
            ],
            options={"ordering": ["organisation__name", "name"], "verbose_name_plural": "categories"},
        ),
        migrations.CreateModel(
            name="SignEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("term", models.CharField(max_length=200)),
                ("slug", models.SlugField()),
                ("video_url", models.URLField()),
                ("description", models.TextField(blank=True)),
                ("usage_context", models.TextField(blank=True)),
                ("tags", models.CharField(blank=True, max_length=300)),
                ("is_quick_reference", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="signs", to="glossary.category"),
                ),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="signs", to="glossary.organisation"),
                ),
            ],
            options={"ordering": ["term"]},
        ),
        migrations.CreateModel(
            name="FAQEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("question", models.CharField(max_length=255)),
                ("answer", models.TextField()),
                (
                    "organisation",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="faqs", to="glossary.organisation"),
                ),
                (
                    "related_category",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="faqs", to="glossary.category"),
                ),
                (
                    "related_sign",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="faqs", to="glossary.signentry"),
                ),
            ],
            options={"ordering": ["question"], "verbose_name": "FAQ entry", "verbose_name_plural": "FAQ entries"},
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(fields=("organisation", "slug"), name="unique_category_slug_per_organisation"),
        ),
        migrations.AddConstraint(
            model_name="signentry",
            constraint=models.UniqueConstraint(fields=("organisation", "slug"), name="unique_sign_slug_per_organisation"),
        ),
    ]
