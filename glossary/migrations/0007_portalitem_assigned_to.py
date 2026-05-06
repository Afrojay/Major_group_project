import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0006_portalitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="portalitem",
            name="assigned_to",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_portal_items", to="glossary.staffprofile"),
        ),
    ]
