from django.core.management.base import BaseCommand

from glossary.models import Category, Organisation, SignEntry


PLACEHOLDER_VIDEO_URL = 'https://example.com/placeholder-isl-video'


class Command(BaseCommand):
    help = 'Load sample organisations, categories and signs for the ISL glossary prototype.'

    def handle(self, *args, **options):
        college = self.create_organisation(
            name='College Computing Department',
            slug='college-computing',
            description='A sample glossary for computing students and staff, focused on common academic and technical terms.',
            theme_colour='#1d4ed8',
        )
        retail = self.create_organisation(
            name='Retail Customer Service',
            slug='retail-customer-service',
            description='A sample glossary for retail staff who need quick access to common customer service signs.',
            theme_colour='#047857',
        )

        college_categories = {
            'programming': 'Programming',
            'databases': 'Databases',
            'networking': 'Networking',
            'assessments': 'Assessments',
            'student-support': 'Student Support',
        }
        retail_categories = {
            'greetings': 'Greetings',
            'payments': 'Payments',
            'refunds': 'Refunds',
            'product-questions': 'Product Questions',
            'customer-support': 'Customer Support',
        }

        college_cats = self.create_categories(college, college_categories)
        retail_cats = self.create_categories(retail, retail_categories)

        self.create_sign(college, college_cats['student-support'], 'Login', 'login', 'A common term used when accessing college systems.', True)
        self.create_sign(college, college_cats['student-support'], 'Password', 'password', 'Used when discussing account access or password reset support.', True)
        self.create_sign(college, college_cats['assessments'], 'Assignment', 'assignment', 'Used for coursework and submitted academic tasks.', True)
        self.create_sign(college, college_cats['assessments'], 'Deadline', 'deadline', 'Used when explaining submission dates or time limits.', True)
        self.create_sign(college, college_cats['databases'], 'Database', 'database', 'A technical term for structured data storage.', False)
        self.create_sign(college, college_cats['programming'], 'Programming', 'programming', 'A general term for writing computer code.', False)
        self.create_sign(college, college_cats['student-support'], 'Help', 'help', 'A useful support sign for asking for assistance.', True)

        self.create_sign(retail, retail_cats['greetings'], 'Hello', 'hello', 'A common greeting for customer interaction.', True)
        self.create_sign(retail, retail_cats['greetings'], 'Thank You', 'thank-you', 'A polite sign used after helping a customer.', True)
        self.create_sign(retail, retail_cats['payments'], 'Cash', 'cash', 'Used when discussing payment by cash.', True)
        self.create_sign(retail, retail_cats['payments'], 'Card', 'card', 'Used when discussing card payment.', True)
        self.create_sign(retail, retail_cats['payments'], 'Receipt', 'receipt', 'Used when asking whether a customer needs a receipt.', True)
        self.create_sign(retail, retail_cats['refunds'], 'Refund', 'refund', 'Used when discussing returned items or refunds.', True)
        self.create_sign(retail, retail_cats['customer-support'], 'Help', 'help', 'Used when asking whether the customer needs assistance.', True)

        self.stdout.write(self.style.SUCCESS('Sample ISL glossary data loaded.'))

    def create_organisation(self, name, slug, description, theme_colour):
        organisation, _ = Organisation.objects.update_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': description,
                'theme_colour': theme_colour,
            },
        )
        return organisation

    def create_categories(self, organisation, category_map):
        categories = {}
        for slug, name in category_map.items():
            category, _ = Category.objects.update_or_create(
                organisation=organisation,
                slug=slug,
                defaults={
                    'name': name,
                    'description': f'Signs related to {name.lower()} in the {organisation.name} context.',
                },
            )
            categories[slug] = category
        return categories

    def create_sign(self, organisation, category, term, slug, description, is_quick_reference):
        SignEntry.objects.update_or_create(
            organisation=organisation,
            slug=slug,
            defaults={
                'category': category,
                'term': term,
                'video_url': PLACEHOLDER_VIDEO_URL,
                'description': description,
                'usage_context': 'This is sample prototype content and should be reviewed before final submission.',
                'tags': f'{term.lower()}, {category.name.lower()}, {organisation.name.lower()}',
                'is_quick_reference': is_quick_reference,
            },
        )
