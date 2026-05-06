from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from glossary.models import Category, FAQEntry, Organisation, PortalItem, SignEntry, StaffProfile


SAMPLE_DATA = [
    {
        "name": "College Computing Department",
        "slug": "college-computing",
        "description": "A sample glossary for computing students and staff, focused on common academic and technical terms.",
        "contact_email": "computing-access@example.com",
        "logo_url": "",
        "theme_colour": "#1d4ed8",
        "staff_username": "college_staff",
        "extra_staff_username": "college_staff_two",
        "manager_username": "college_manager",
        "glossary_manager_username": "college_glossary",
        "categories": {
            "Programming": ["Function", "Variable", "Loop", "Debugging"],
            "Databases": ["Database", "Query", "Table"],
            "Student Support": ["Login", "Password", "Assignment"],
        },
        "portal_items": [
            ("calendar_event", "Lab support hour", "Drop-in support for login, password, and assignment vocabulary."),
            ("calendar_event", "Assessment week reminder", "Review common student support signs before the help desk rush."),
        ],
    },
    {
        "name": "Retail Customer Service",
        "slug": "retail-customer-service",
        "description": "A sample glossary for retail staff who need quick access to common customer service signs.",
        "contact_email": "retail-access@example.com",
        "logo_url": "",
        "theme_colour": "#047857",
        "staff_username": "retail_staff",
        "extra_staff_username": "retail_staff_two",
        "manager_username": "retail_manager",
        "glossary_manager_username": "retail_glossary",
        "categories": {
            "Greetings": ["Hello", "Thank you", "Can I help?"],
            "Payments": ["Card", "Cash", "Receipt"],
            "Store Support": ["Refund", "Exchange", "Queue"],
        },
        "portal_items": [
            ("task", "Check refund desk signs", "Review refund and exchange signs before opening."),
            ("task", "Queue support handover", "Make sure floor staff know where quick reference signs are."),
        ],
    },
    {
        "name": "Healthcare Reception",
        "slug": "healthcare-reception",
        "description": "A sample glossary for healthcare reception and frontline clinic staff, focused on everyday access and appointment support.",
        "contact_email": "healthcare-access@example.com",
        "logo_url": "",
        "theme_colour": "#7c3aed",
        "staff_username": "healthcare_staff",
        "extra_staff_username": "healthcare_staff_two",
        "manager_username": "healthcare_manager",
        "glossary_manager_username": "healthcare_glossary",
        "categories": {
            "Appointments": ["Appointment", "Waiting room", "Doctor", "Nurse"],
            "Reception": ["Name", "Date of birth", "Address", "Interpreter"],
            "Care Support": ["Pain", "Medication", "Emergency", "Help"],
        },
        "portal_items": [
            ("appointment", "Interpreter requested", "Reception reminder for a 10:15 appointment."),
            ("appointment", "New patient check-in", "Prepare name, date of birth, and waiting room signs."),
        ],
    },
]


class Command(BaseCommand):
    help = "Load or refresh sample organisations, categories, signs, and FAQs."

    def handle(self, *args, **options):
        for organisation_data in SAMPLE_DATA:
            organisation, _ = Organisation.objects.update_or_create(
                slug=organisation_data["slug"],
                defaults={
                    "name": organisation_data["name"],
                    "description": organisation_data["description"],
                    "contact_email": organisation_data["contact_email"],
                    "logo_url": organisation_data["logo_url"],
                    "theme_colour": organisation_data["theme_colour"],
                },
            )
            for category_name, terms in organisation_data["categories"].items():
                category, _ = Category.objects.update_or_create(
                    organisation=organisation,
                    slug=slugify(category_name),
                    defaults={
                        "name": category_name,
                        "description": f"Signs related to {category_name.lower()} in the {organisation.name} context.",
                    },
                )
                for term in terms:
                    SignEntry.objects.update_or_create(
                        organisation=organisation,
                        slug=slugify(term),
                        defaults={
                            "category": category,
                            "term": term,
                            "video_url": "https://example.com/placeholder-isl-video",
                            "description": f"A common service term for {organisation.name}.",
                            "usage_context": "This is sample prototype content and should be reviewed before final submission.",
                            "tags": f"{term.lower()}, {category_name.lower()}, {organisation.name.lower()}",
                            "is_quick_reference": term
                            in {
                                "Login",
                                "Password",
                                "Hello",
                                "Thank you",
                                "Refund",
                                "Appointment",
                                "Interpreter",
                                "Emergency",
                                "Help",
                            },
                        },
                    )
            FAQEntry.objects.update_or_create(
                organisation=organisation,
                question="Is this a complete ISL dictionary?",
                defaults={
                    "answer": "No. This prototype is an organisation-specific glossary support tool, not a complete national dictionary or replacement for interpreters.",
                },
            )
            user, created = User.objects.get_or_create(
                username=organisation_data["staff_username"],
                defaults={"email": f"{organisation_data['staff_username']}@example.com"},
            )
            if created:
                user.set_password("prototype123")
                user.save()
            StaffProfile.objects.update_or_create(
                user=user,
                defaults={
                    "organisation": organisation,
                    "role": "Sample staff user",
                    "role_type": StaffProfile.RoleType.STAFF,
                },
            )
            extra_user, created = User.objects.get_or_create(
                username=organisation_data["extra_staff_username"],
                defaults={"email": f"{organisation_data['extra_staff_username']}@example.com"},
            )
            if created:
                extra_user.set_password("prototype123")
                extra_user.save()
            extra_profile, _ = StaffProfile.objects.update_or_create(
                user=extra_user,
                defaults={
                    "organisation": organisation,
                    "role": "Sample staff user",
                    "role_type": StaffProfile.RoleType.STAFF,
                },
            )
            manager_user, created = User.objects.get_or_create(
                username=organisation_data["manager_username"],
                defaults={
                    "email": f"{organisation_data['manager_username']}@example.com",
                },
            )
            if created:
                manager_user.set_password("prototype123")
                manager_user.save()
            StaffProfile.objects.update_or_create(
                user=manager_user,
                defaults={
                    "organisation": organisation,
                    "role": "Service manager",
                    "role_type": StaffProfile.RoleType.MANAGER,
                },
            )
            glossary_user, created = User.objects.get_or_create(
                username=organisation_data["glossary_manager_username"],
                defaults={
                    "email": f"{organisation_data['glossary_manager_username']}@example.com",
                    "is_staff": True,
                },
            )
            if created:
                glossary_user.set_password("prototype123")
                glossary_user.save()
            StaffProfile.objects.update_or_create(
                user=glossary_user,
                defaults={
                    "organisation": organisation,
                    "role": "Glossary manager",
                    "role_type": StaffProfile.RoleType.GLOSSARY_MANAGER,
                },
            )
            for index, (item_type, title, description) in enumerate(organisation_data["portal_items"]):
                PortalItem.objects.update_or_create(
                    organisation=organisation,
                    title=title,
                    defaults={
                        "item_type": item_type,
                        "description": description,
                        "due_at": timezone.now() + timezone.timedelta(days=index),
                    },
                )
            PortalItem.objects.update_or_create(
                organisation=organisation,
                title="Assigned accessibility follow-up",
                defaults={
                    "assigned_to": extra_profile,
                    "created_by": extra_profile,
                    "item_type": PortalItem.ItemType.TASK,
                    "description": "Sample assigned task for the staff task board.",
                    "due_at": timezone.now() + timezone.timedelta(days=1),
                },
            )
        self.stdout.write(self.style.SUCCESS("Sample ISL glossary data loaded. Demo password: prototype123"))
