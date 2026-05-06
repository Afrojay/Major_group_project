from django.db import migrations, models


def copy_admin_flag_to_role_type(apps, schema_editor):
    StaffProfile = apps.get_model("glossary", "StaffProfile")
    for profile in StaffProfile.objects.all():
        if getattr(profile, "is_organisation_admin", False):
            profile.role_type = "glossary_manager"
            profile.save(update_fields=["role_type"])


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0003_org_admin_public_requests"),
    ]

    operations = [
        migrations.AddField(
            model_name="staffprofile",
            name="role_type",
            field=models.CharField(
                choices=[
                    ("staff", "Staff"),
                    ("manager", "Manager"),
                    ("glossary_manager", "Glossary manager"),
                ],
                default="staff",
                max_length=30,
            ),
        ),
        migrations.RunPython(copy_admin_flag_to_role_type, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="staffprofile",
            name="is_organisation_admin",
        ),
        migrations.AlterField(
            model_name="signrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending manager review"),
                    ("needs_clarification", "Needs clarification"),
                    ("manager_approved", "Manager approved"),
                    ("sent_to_interpreter", "Sent to interpreter"),
                    ("completed", "Completed"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=30,
            ),
        ),
    ]
