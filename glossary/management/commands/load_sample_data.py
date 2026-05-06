from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth.models import User

from glossary.models import Category, FAQEntry, Organisation, SignEntry, StaffProfile


SAMPLE_DATA = [
    {
        "name": "College Computing Department",
        "slug": "college-computing",
        "description": "A sample glossary for computing students and staff, focused on common academic and technical terms.",
        "theme_colour": "#1d4ed8",
        "staff_username": "college_staff",
        "admin_username": "college_admin",
        "categories": {
            "Programming": ["Function", "Variable", "Loop", "Debugging"],
            "Databases": ["Database", "Query", "Table"],
            "Student Support": ["Login", "Password", "Assignment"],
        },
    },
    {
        "name": "Retail Customer Service",
        "slug": "retail-customer-service",
        "description": "A sample glossary for retail staff who need quick access to common customer service signs.",
        "theme_colour": "#047857",
        "staff_username": "retail_staff",
        "admin_username": "retail_admin",
        "categories": {
            "Greetings": ["Hello", "Thank you", "Can I help?"],
            "Payments": ["Card", "Cash", "Receipt"],
            "Store Support": ["Refund", "Exchange", "Queue"],
        },
    },
    {
        "name": "Healthcare Reception",
        "slug": "healthcare-reception",
        "description": "A sample glossary for healthcare reception and frontline clinic staff, focused on everyday access and appointment support.",
        "theme_colour": "#0f766e",
        "staff_username": "healthcare_staff",
        "admin_username": "healthcare_admin",
        "categories": {
            "Appointments": ["Appointment", "Waiting room", "Doctor", "Nurse"],
            "Reception": ["Name", "Date of birth", "Address", "Interpreter"],
            "Care Support": ["Pain", "Medication", "Emergency", "Help"],
        },
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
                    "is_organisation_admin": False,
                },
            )
            admin_user, created = User.objects.get_or_create(
                username=organisation_data["admin_username"],
                defaults={
                    "email": f"{organisation_data['admin_username']}@example.com",
                    "is_staff": True,
                },
            )
            if created:
                admin_user.set_password("prototype123")
                admin_user.save()
            StaffProfile.objects.update_or_create(
                user=admin_user,
                defaults={
                    "organisation": organisation,
                    "role": "Organisation glossary admin",
                    "is_organisation_admin": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Sample ISL glossary data loaded. Demo password: prototype123"))
