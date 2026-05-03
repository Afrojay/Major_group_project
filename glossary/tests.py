from django.test import TestCase
from django.urls import reverse

from .models import Category, Organisation, SignEntry


class GlossaryPageTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(
            name='Retail Customer Service',
            slug='retail-customer-service',
            description='Sample retail glossary.',
        )
        self.category = Category.objects.create(
            organisation=self.organisation,
            name='Payments',
            slug='payments',
            description='Payment-related signs.',
        )
        self.sign = SignEntry.objects.create(
            organisation=self.organisation,
            category=self.category,
            term='Receipt',
            slug='receipt',
            video_url='https://example.com/placeholder-isl-video',
            description='Used when asking whether a customer needs a receipt.',
            tags='receipt, payment, retail',
            is_quick_reference=True,
        )
        self.non_quick_sign = SignEntry.objects.create(
            organisation=self.organisation,
            category=self.category,
            term='Voucher',
            slug='voucher',
            video_url='https://example.com/placeholder-isl-video',
            description='Used when discussing a shop voucher.',
            tags='voucher, payment, retail',
            is_quick_reference=False,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('glossary:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Retail Customer Service')

    def test_organisation_page_loads(self):
        response = self.client.get(reverse('glossary:organisation_home', args=[self.organisation.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payments')

    def test_category_page_loads(self):
        response = self.client.get(reverse('glossary:category_detail', args=[self.organisation.slug, self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Receipt')

    def test_sign_detail_page_loads(self):
        response = self.client.get(reverse('glossary:sign_detail', args=[self.organisation.slug, self.sign.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Receipt')

    def test_search_returns_expected_sign(self):
        response = self.client.get(reverse('glossary:search_results', args=[self.organisation.slug]), {'q': 'receipt'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Receipt')

    def test_quick_reference_only_shows_quick_reference_signs(self):
        response = self.client.get(reverse('glossary:quick_reference', args=[self.organisation.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Receipt')
        self.assertNotContains(response, 'Voucher')
