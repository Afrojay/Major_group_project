from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Category, FavouriteSign, Organisation, PortalItem, SignEntry, SignRequest, StaffProfile, Transcript


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
        self.second_user = User.objects.create_user(username="stafftwo", password="pass12345")
        self.second_profile = StaffProfile.objects.create(user=self.second_user, organisation=self.org)
        self.manager_user = User.objects.create_user(username="manager", password="pass12345")
        self.manager_profile = StaffProfile.objects.create(
            user=self.manager_user,
            organisation=self.org,
            role_type=StaffProfile.RoleType.MANAGER,
        )

    def test_search_is_scoped_to_organisation(self):
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]), {"q": "Refund"})
        self.assertContains(response, "No signs matched this search.")
        self.assertNotContains(response, reverse("sign_detail", args=[self.other_org.slug, self.other_sign.slug]))

    def test_category_filter_limits_signs_on_organisation_page(self):
        other_category = Category.objects.create(
            organisation=self.org,
            name="Other",
            slug="other",
        )
        SignEntry.objects.create(
            organisation=self.org,
            category=other_category,
            term="Hidden",
            slug="hidden",
            video_url="https://example.com/hidden",
        )
        response = self.client.get(
            reverse("organisation_home", args=[self.org.slug]),
            {"category": self.category.slug},
        )
        self.assertContains(response, "Support signs")
        self.assertContains(response, "Login")
        self.assertNotContains(response, "Hidden")

    def test_nav_uses_accessible_collapsible_menu(self):
        response = self.client.get(reverse("organisation_list"))
        self.assertContains(response, '<details class="nav-menu">')
        self.assertContains(response, "<summary>Menu</summary>")

    def test_organisation_page_renders_branding_content(self):
        self.org.description = "Computing support glossary."
        self.org.contact_email = "support@example.com"
        self.org.logo_url = "https://example.com/logo.png"
        self.org.theme_colour = "#123abc"
        self.org.save()
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertContains(response, "College")
        self.assertContains(response, "Computing support glossary.")
        self.assertContains(response, "support@example.com")
        self.assertContains(response, 'src="https://example.com/logo.png"')
        self.assertContains(response, 'alt="College logo"')
        self.assertContains(response, "--accent: #123abc")

    def test_login_redirect_sends_staff_to_their_dashboard(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("dashboard_redirect"))
        self.assertRedirects(response, reverse("staff_dashboard", args=[self.org.slug]))

    def test_login_form_redirects_staff_to_their_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "staff", "password": "pass12345"},
        )
        self.assertRedirects(response, reverse("dashboard_redirect"), fetch_redirect_response=False)
        response = self.client.get(response.url)
        self.assertRedirects(response, reverse("staff_dashboard", args=[self.org.slug]))

    def test_login_shows_welcome_message(self):
        response = self.client.post(
            reverse("login"),
            {"username": "staff", "password": "pass12345"},
            follow=True,
        )
        self.assertContains(response, "Welcome back, staff - College.")

    def test_login_form_redirects_manager_to_manager_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "manager", "password": "pass12345"},
        )
        self.assertRedirects(response, reverse("dashboard_redirect"), fetch_redirect_response=False)
        response = self.client.get(response.url)
        self.assertRedirects(response, reverse("manager_dashboard", args=[self.org.slug]))

    def test_staff_menu_contains_staff_shortcuts(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Organisation glossary")
        self.assertContains(response, "My tasks")
        self.assertContains(response, "Saved signs")
        self.assertContains(response, "My requests")
        self.assertNotContains(response, "Assign tasks")

    def test_manager_menu_contains_manager_shortcuts(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Manager dashboard")
        self.assertContains(response, "Review requests")
        self.assertContains(response, "Assign tasks")
        self.assertNotContains(response, "My tasks")

    def test_staff_dashboard_uses_organisation_theme_and_role_label(self):
        self.org.theme_colour = "#123abc"
        self.org.save()
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[self.org.slug]))
        self.assertContains(response, "--accent: #123abc")
        self.assertContains(response, "Welcome to College")
        self.assertContains(response, "Hi staff")
        self.assertContains(response, "Staff portal")
        self.assertContains(response, "Local time:")
        self.assertContains(response, 'href="#favourite-signs"')
        self.assertContains(response, 'href="#sign-requests"')
        self.assertContains(response, 'href="#recent-signs"')
        self.assertContains(response, 'id="favourite-signs"')
        self.assertContains(response, 'id="sign-requests"')

    def test_manager_dashboard_uses_organisation_theme(self):
        self.org.theme_colour = "#123abc"
        self.org.save()
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertContains(response, "--accent: #123abc")
        self.assertContains(response, "Welcome to College")
        self.assertContains(response, "Hi manager")

    def test_sign_and_request_pages_use_organisation_theme(self):
        self.org.theme_colour = "#123abc"
        self.org.save()
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertContains(response, "--accent: #123abc")
        response = self.client.get(reverse("request_sign", args=[self.org.slug]))
        self.assertContains(response, "--accent: #123abc")

    def test_sign_detail_renders_optional_transcript_and_thumbnail(self):
        self.sign.thumbnail_url = "https://example.com/login-thumb.jpg"
        self.sign.save()
        Transcript.objects.create(sign=self.sign, text="Transcript text for the login sign.")
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertContains(response, "Transcript text for the login sign.")
        self.assertContains(response, 'src="https://example.com/login-thumb.jpg"')
        self.assertContains(response, 'alt="Thumbnail for Login ISL video"')

    def test_retail_dashboard_shows_retail_placeholder_widgets(self):
        retail_user = User.objects.create_user(username="retail", password="pass12345")
        StaffProfile.objects.create(user=retail_user, organisation=self.other_org)
        self.client.login(username="retail", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[self.other_org.slug]))
        self.assertContains(response, "Clock-in reminder")
        self.assertContains(response, "floor tasks")

    def test_healthcare_dashboard_shows_appointment_placeholder_widgets(self):
        healthcare = Organisation.objects.create(
            name="Healthcare Reception",
            slug="healthcare-reception",
        )
        healthcare_user = User.objects.create_user(username="healthcare", password="pass12345")
        StaffProfile.objects.create(user=healthcare_user, organisation=healthcare)
        self.client.login(username="healthcare", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[healthcare.slug]))
        self.assertContains(response, "Upcoming appointments")
        self.assertContains(response, "+ Add appointment")
        self.assertContains(response, "Accessibility needs")

    def test_staff_can_add_dashboard_item_for_own_organisation(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("create_portal_item", args=[self.org.slug]),
            {
                "title": "Desk handover",
                "description": "Review support signs before the afternoon shift.",
            },
        )
        self.assertRedirects(response, reverse("staff_dashboard", args=[self.org.slug]))
        item = PortalItem.objects.get(title="Desk handover")
        self.assertEqual(item.organisation, self.org)
        self.assertEqual(item.created_by, self.profile)

    def test_staff_can_mark_dashboard_item_complete(self):
        item = PortalItem.objects.create(
            organisation=self.org,
            created_by=self.profile,
            item_type=PortalItem.ItemType.CALENDAR_EVENT,
            title="Support slot",
        )
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(reverse("complete_portal_item", args=[self.org.slug, item.id]))
        self.assertRedirects(response, reverse("staff_dashboard", args=[self.org.slug]))
        item.refresh_from_db()
        self.assertTrue(item.is_complete)

    def test_manager_can_assign_task_to_staff(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.post(
            reverse("create_assigned_task", args=[self.org.slug]),
            {
                "assigned_to": self.second_profile.id,
                "title": "Review front desk signs",
                "description": "Check quick reference terms before opening.",
            },
        )
        self.assertRedirects(response, reverse("manager_dashboard", args=[self.org.slug]))
        task = PortalItem.objects.get(title="Review front desk signs")
        self.assertEqual(task.assigned_to, self.second_profile)
        self.assertEqual(task.created_by, self.manager_profile)
        self.assertEqual(task.item_type, PortalItem.ItemType.TASK)

    def test_manager_dashboard_contains_task_assignment_workspace(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Assign staff tasks")
        self.assertContains(response, 'name="assigned_to"')
        self.assertNotContains(response, "Staff dashboard")

    def test_manager_is_redirected_from_staff_dashboard_to_manager_dashboard(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[self.org.slug]))
        self.assertRedirects(response, reverse("manager_dashboard", args=[self.org.slug]))

    def test_manager_is_redirected_from_staff_task_board_to_manager_dashboard(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("task_board", args=[self.org.slug]))
        self.assertRedirects(response, reverse("manager_dashboard", args=[self.org.slug]))

    def test_staff_task_board_only_shows_assigned_tasks(self):
        assigned = PortalItem.objects.create(
            organisation=self.org,
            assigned_to=self.profile,
            item_type=PortalItem.ItemType.TASK,
            title="Assigned task",
        )
        PortalItem.objects.create(
            organisation=self.org,
            assigned_to=self.second_profile,
            item_type=PortalItem.ItemType.TASK,
            title="Other staff task",
        )
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("task_board", args=[self.org.slug]))
        self.assertContains(response, assigned.title)
        self.assertNotContains(response, "Other staff task")

    def test_staff_can_complete_assigned_task(self):
        task = PortalItem.objects.create(
            organisation=self.org,
            assigned_to=self.profile,
            item_type=PortalItem.ItemType.TASK,
            title="Assigned task",
        )
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("complete_portal_item", args=[self.org.slug, task.id]),
            {"next": reverse("task_board", args=[self.org.slug])},
        )
        self.assertRedirects(response, reverse("task_board", args=[self.org.slug]))
        task.refresh_from_db()
        self.assertTrue(task.is_complete)

    def test_staff_cannot_complete_task_assigned_to_someone_else(self):
        task = PortalItem.objects.create(
            organisation=self.org,
            assigned_to=self.second_profile,
            item_type=PortalItem.ItemType.TASK,
            title="Other staff task",
        )
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(reverse("complete_portal_item", args=[self.org.slug, task.id]))
        self.assertEqual(response.status_code, 404)
        task.refresh_from_db()
        self.assertFalse(task.is_complete)

    def test_staff_cannot_complete_other_organisation_dashboard_item(self):
        item = PortalItem.objects.create(
            organisation=self.other_org,
            item_type=PortalItem.ItemType.TASK,
            title="Other org task",
        )
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(reverse("complete_portal_item", args=[self.org.slug, item.id]))
        self.assertEqual(response.status_code, 404)
        item.refresh_from_db()
        self.assertFalse(item.is_complete)

    def test_organisation_logo_only_renders_when_configured(self):
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertNotContains(response, "org-logo")
        self.org.logo_url = "https://example.com/logo.png"
        self.org.save()
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertContains(response, "org-logo")

    def test_invalid_theme_colour_falls_back_in_page_output(self):
        Organisation.objects.filter(id=self.org.id).update(theme_colour="bad; color:red")
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertContains(response, "--accent: #0d6efd")
        self.assertNotContains(response, "bad; color:red")

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

    def test_staff_request_form_does_not_ask_for_contact_details(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("request_sign", args=[self.org.slug]))
        self.assertContains(response, "linked to your College staff profile")
        self.assertNotContains(response, 'name="requester_name"')
        self.assertNotContains(response, 'name="requester_email"')

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

    def test_visitor_request_form_requires_contact_details(self):
        response = self.client.get(reverse("request_sign", args=[self.org.slug]))
        self.assertContains(response, 'name="requester_name"')
        self.assertContains(response, 'name="requester_email"')

    def test_manager_can_approve_request_for_interpreter_review(self):
        sign_request = SignRequest.objects.create(
            organisation=self.org,
            requested_by=self.profile,
            term="Directions",
            context="Needed at reception.",
        )
        self.client.login(username="manager", password="pass12345")
        response = self.client.post(
            reverse("review_sign_request", args=[self.org.slug, sign_request.id]),
            {
                "status": SignRequest.Status.MANAGER_APPROVED,
                "admin_notes": "Suitable for interpreter review.",
            },
        )
        self.assertRedirects(response, reverse("manager_dashboard", args=[self.org.slug]))
        sign_request.refresh_from_db()
        self.assertEqual(sign_request.status, SignRequest.Status.MANAGER_APPROVED)
        self.assertEqual(sign_request.admin_notes, "Suitable for interpreter review.")

    def test_manager_review_cannot_mark_request_as_interpreter_completed(self):
        sign_request = SignRequest.objects.create(
            organisation=self.org,
            requested_by=self.profile,
            term="Directions",
            context="Needed at reception.",
        )
        self.client.login(username="manager", password="pass12345")
        self.client.post(
            reverse("review_sign_request", args=[self.org.slug, sign_request.id]),
            {
                "status": SignRequest.Status.COMPLETED,
                "admin_notes": "Trying to skip interpreter review.",
            },
        )
        sign_request.refresh_from_db()
        self.assertEqual(sign_request.status, SignRequest.Status.PENDING)

    def test_staff_member_cannot_open_manager_dashboard(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
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

    def test_model_validation_requires_public_request_contact_details(self):
        sign_request = SignRequest(
            organisation=self.org,
            term="Directions",
            context="Needed at reception.",
        )
        with self.assertRaises(ValidationError):
            sign_request.full_clean()
