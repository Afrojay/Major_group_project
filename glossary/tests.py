from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Category, FavouriteSign, Organisation, SignEntry, SignRequest, StaffProfile


class GlossaryWorkflowTests(TestCase):
    def setUp(self):
        self.org = Organisation.objects.create(name="College", slug="college")
        self.other_org = Organisation.objects.create(name="Retail", slug="retail")
        self.category = Category.objects.create(
            organisation=self.org,
            name="Support",
            slug="support",
        )
        self.other_category = Category.objects.create(
            organisation=self.other_org,
            name="Payments",
            slug="payments",
        )
        self.sign = SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Login",
            slug="login",
            video_url="https://example.com/login",
        )
        self.other_sign = SignEntry.objects.create(
            organisation=self.other_org,
            category=self.other_category,
            term="Refund",
            slug="refund",
            video_url="https://example.com/refund",
        )
        self.user = User.objects.create_user(username="staff", password="pass12345")
        self.profile = StaffProfile.objects.create(user=self.user, organisation=self.org)
        self.admin_user = User.objects.create_user(username="orgadmin", password="pass12345")
        self.admin_profile = StaffProfile.objects.create(
            user=self.admin_user,
            organisation=self.org,
            is_organisation_admin=True,
        )

    def test_search_is_scoped_to_organisation(self):
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]), {"q": "Refund"})
        self.assertContains(response, "No signs matched this search.")
        self.assertNotContains(response, reverse("sign_detail", args=[self.other_org.slug, self.other_sign.slug]))

    def test_staff_can_favourite_own_organisation_sign(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("toggle_favourite", args=[self.org.slug, self.sign.id]),
            {"next": reverse("sign_detail", args=[self.org.slug, self.sign.slug])},
        )
        self.assertRedirects(response, reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertTrue(FavouriteSign.objects.filter(staff_profile=self.profile, sign=self.sign).exists())

    def test_staff_cannot_favourite_other_organisation_sign(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(reverse("toggle_favourite", args=[self.other_org.slug, self.other_sign.id]))
        self.assertEqual(response.status_code, 404)
        self.assertFalse(FavouriteSign.objects.exists())

    def test_staff_request_is_pending_and_org_scoped(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("request_sign", args=[self.org.slug]),
            {
                "term": "Password reset",
                "suggested_category": self.category.id,
                "context": "Needed at the IT help desk.",
            },
        )
        self.assertRedirects(response, reverse("staff_dashboard", args=[self.org.slug]))
        sign_request = SignRequest.objects.get()
        self.assertEqual(sign_request.organisation, self.org)
        self.assertEqual(sign_request.requested_by, self.profile)
        self.assertEqual(sign_request.status, SignRequest.Status.PENDING)

    def test_visitor_can_submit_request_with_email(self):
        response = self.client.post(
            reverse("request_sign", args=[self.org.slug]),
            {
                "requester_name": "Visitor",
                "requester_email": "visitor@example.com",
                "term": "Directions",
                "suggested_category": self.category.id,
                "context": "Needed at the reception desk.",
            },
        )
        self.assertRedirects(response, reverse("organisation_home", args=[self.org.slug]))
        sign_request = SignRequest.objects.get(term="Directions")
        self.assertIsNone(sign_request.requested_by)
        self.assertEqual(sign_request.requester_email, "visitor@example.com")
        self.assertEqual(sign_request.status, SignRequest.Status.PENDING)

    def test_org_admin_can_review_request_for_own_org(self):
        sign_request = SignRequest.objects.create(
            organisation=self.org,
            requested_by=self.profile,
            term="Directions",
            context="Needed at reception.",
        )
        self.client.login(username="orgadmin", password="pass12345")
        response = self.client.post(
            reverse("review_sign_request", args=[self.org.slug, sign_request.id]),
            {
                "status": SignRequest.Status.NEEDS_CLARIFICATION,
                "admin_notes": "Ask for more context.",
            },
        )
        self.assertRedirects(response, reverse("organisation_admin_dashboard", args=[self.org.slug]))
        sign_request.refresh_from_db()
        self.assertEqual(sign_request.status, SignRequest.Status.NEEDS_CLARIFICATION)
        self.assertEqual(sign_request.admin_notes, "Ask for more context.")

    def test_staff_member_cannot_open_org_admin_dashboard(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("organisation_admin_dashboard", args=[self.org.slug]))
        self.assertEqual(response.status_code, 404)

    def test_model_validation_rejects_cross_organisation_sign_category(self):
        sign = SignEntry(
            organisation=self.org,
            category=self.other_category,
            term="Cross scoped",
            slug="cross-scoped",
            video_url="https://example.com/cross",
        )
        with self.assertRaises(ValidationError):
            sign.full_clean()

    def test_model_validation_rejects_cross_organisation_request_category(self):
        sign_request = SignRequest(
            organisation=self.org,
            requested_by=self.profile,
            suggested_category=self.other_category,
            term="Receipt",
            context="Needed at reception.",
        )
        with self.assertRaises(ValidationError):
            sign_request.full_clean()
