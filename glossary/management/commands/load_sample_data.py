from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from glossary.models import Category, FAQEntry, Organisation, PortalItem, SignEntry, StaffProfile


FALLBACK_VIDEO_URL = "https://example.com/isl-video-under-review"

# Only a small number of project signs have clear candidate ISL video references.
# Other signs are marked as needing review because many online results are ASL/BSL
# rather than Irish Sign Language.
CANDIDATE_VIDEO_SOURCES = {
    "Hello": {
        "video_url": "https://www.youtube.com/embed/wr-_YGz7oAc",
        "source_label": "DIT Sign Language Society - Basic Phrases in Irish Sign Language 01",
        "source_url": "https://www.youtube.com/watch?v=wr-_YGz7oAc",
        "source_note": "Candidate external ISL video. This general phrases video includes Hello/Goodbye and other basic ISL phrases.",
    },
    "Thank you": {
        "video_url": "https://www.youtube.com/embed/gtQMAY1wSq0",
        "source_label": "Irish Deaf Society - Irish Sign Language for Thank you",
        "source_url": "https://www.youtube.com/watch?v=gtQMAY1wSq0",
        "source_note": "Candidate external ISL video from the Irish Deaf Society.",
    },
    "Doctor": {
        "video_url": "https://www.youtube.com/embed/SumBkLk1HDQ",
        "source_label": "Doctor in Irish Sign Language",
        "source_url": "https://www.youtube.com/watch?v=SumBkLk1HDQ",
        "source_note": "Candidate external ISL video. Healthcare vocabulary should still be reviewed before real use.",
    },
    "Nurse": {
        "video_url": "https://www.youtube.com/embed/ZvqREs7aaK0",
        "source_label": "Nurse in Irish Sign Language",
        "source_url": "https://www.youtube.com/watch?v=ZvqREs7aaK0",
        "source_note": "Candidate external ISL video. Healthcare vocabulary should still be reviewed before real use.",
    },
}


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


def video_details_for(term):
    if term in CANDIDATE_VIDEO_SOURCES:
        details = CANDIDATE_VIDEO_SOURCES[term]
        return {
            "video_url": details["video_url"],
            "usage_context_extra": f"Video source: {details['source_label']} ({details['source_url']}). {details['source_note']}",
            "is_official_published": False,
        }
    return {
        "video_url": FALLBACK_VIDEO_URL,
        "usage_context_extra": "Video status: Needs review. A suitable verified ISL video was not available during initial content sourcing, so this sign needs later review or custom content.",
        "is_official_published": False,
    }


def usage_context_for(organisation, category_name, term, video_note):
    return (
        f"Used in the {organisation.name} context for {category_name.lower()} situations. "
        f"{video_note}"
    )


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
                    video_details = video_details_for(term)
                    SignEntry.objects.update_or_create(
                        organisation=organisation,
                        slug=slugify(term),
                        defaults={
                            "category": category,
                            "term": term,
                            "video_url": video_details["video_url"],
                            "description": f"A common service term for {organisation.name}.",
                            "usage_context": usage_context_for(
                                organisation,
                                category_name,
                                term,
                                video_details["usage_context_extra"],
                            ),
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
                            "is_official_published": video_details["is_official_published"],
                        },
                    )
            FAQEntry.objects.update_or_create(
                organisation=organisation,
                question="Is this a complete ISL dictionary?",
                defaults={
                    "answer": "No. This prototype is an organisation-specific glossary support tool, not a complete national dictionary or replacement for interpreters.",
                },
            )
            FAQEntry.objects.update_or_create(
                organisation=organisation,
                question="Why do some signs need video review?",
                defaults={
                    "answer": "Some signs are marked as needing video review because suitable verified Irish Sign Language videos were not found during initial content sourcing. Many online results were for ASL or BSL rather than ISL, so final deployment would require reviewed ISL content.",
                },
            )
            FAQEntry.objects.update_or_create(
                organisation=organisation,
                question="Where can I find wider ISL resources?",
                defaults={
                    "answer": "This prototype should be used as a local glossary support tool only. For wider ISL learning, dictionary resources, Deaf awareness information, and interpreter support, users should consult recognised ISL and Deaf community organisations such as the Irish Deaf Society, DCU ISL STEM Glossary, SLIS/IRIS, and relevant public-service accessibility information.",
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
                    "role": "Staff user",
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
                    "role": "Staff user",
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
                    "description": "Assigned task for the staff task board.",
                    "due_at": timezone.now() + timezone.timedelta(days=1),
                },
            )
        self.stdout.write(self.style.SUCCESS("Demo ISL glossary data loaded. Password: prototype123"))
