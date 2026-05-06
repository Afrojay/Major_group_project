import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0004_staff_roles_request_review_statuses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="theme_colour",
            field=models.CharField(
                default="#0d6efd",
                max_length=20,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Enter a valid six-digit hex colour, for example #0d6efd.",
                        regex="^#[0-9A-Fa-f]{6}$",
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="organisation",
            name="logo_url",
            field=models.URLField(blank=True),
        ),
    ]
