from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0002_staff_favourites_requests"),
    ]

    operations = [
        migrations.AddField(
            model_name="staffprofile",
            name="is_organisation_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="signrequest",
            name="requester_email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="signrequest",
            name="requester_name",
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
