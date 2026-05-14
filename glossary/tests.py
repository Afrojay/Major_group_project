from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from glossary.management.commands.load_sample_data import description_for

from .models import (
    Category,
    FavouriteSign,
    Organisation,
    PortalItem,
    SignEntry,
    SignEntryChangeLog,
    SignRequest,
    StaffProfile,
    Transcript,
)


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
        self.glossary_user = User.objects.create_user(
            username="glossary",
            password="pass12345",
        )
        self.glossary_profile = StaffProfile.objects.create(
            user=self.glossary_user,
            organisation=self.org,
            role_type=StaffProfile.RoleType.GLOSSARY_MANAGER,
        )
        self.platform_admin = User.objects.create_superuser(
            username="platform",
            email="platform@example.com",
            password="pass12345",
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

    def test_signs_api_returns_filtered_organisation_results_for_vue(self):
        SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Password reset",
            slug="password-reset",
            video_url="https://example.com/password-reset",
            tags="account, support",
        )
        response = self.client.get(
            reverse("organisation_signs_api", args=[self.org.slug]),
            {"q": "password", "category": self.category.slug, "letter": "P"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["organisation"]["slug"], self.org.slug)
        self.assertEqual(payload["filters"]["q"], "password")
        self.assertEqual(payload["filters"]["category"], self.category.slug)
        self.assertEqual(payload["filters"]["letter"], "P")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["term"], "Password reset")
        self.assertEqual(payload["results"][0]["category"]["name"], "Support")
        self.assertEqual(payload["results"][0]["tags"], ["account", "support"])
        self.assertEqual(
            payload["results"][0]["tag_links"][1]["url"],
            reverse("category_detail", args=[self.org.slug, self.category.slug]),
        )
        self.assertNotContains(response, "Refund")

    def test_signs_api_marks_staff_favourites_for_vue(self):
        FavouriteSign.objects.create(staff_profile=self.profile, sign=self.sign)
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("organisation_signs_api", args=[self.org.slug]))
        payload = response.json()
        login_result = next(item for item in payload["results"] if item["term"] == "Login")
        self.assertTrue(login_result["is_favourite"])
        self.assertTrue(login_result["can_favourite"])
        self.assertEqual(login_result["favourite_url"], reverse("toggle_favourite", args=[self.org.slug, self.sign.id]))

    def test_signs_api_does_not_offer_favourites_to_visitors(self):
        response = self.client.get(reverse("organisation_signs_api", args=[self.org.slug]))
        payload = response.json()
        login_result = next(item for item in payload["results"] if item["term"] == "Login")
        self.assertFalse(login_result["can_favourite"])
        self.assertFalse(login_result["is_favourite"])

    def test_signs_api_rejects_cross_organisation_category_filter(self):
        response = self.client.get(
            reverse("organisation_signs_api", args=[self.org.slug]),
            {"category": self.other_category.slug},
        )
        self.assertEqual(response.status_code, 404)

    def test_nav_uses_accessible_collapsible_menu(self):
        response = self.client.get(reverse("organisation_list"))
        self.assertContains(response, '<details class="nav-menu">')
        self.assertContains(response, "<summary>Menu</summary>")

    def test_flash_messages_are_dismissible(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("toggle_favourite", args=[self.org.slug, self.sign.id]),
            {"next": reverse("sign_detail", args=[self.org.slug, self.sign.slug])},
            follow=True,
        )
        self.assertContains(response, "data-auto-dismiss-messages")
        self.assertContains(response, "data-dismiss-message")
        self.assertContains(response, "messages.js")

    def test_sample_descriptions_are_dictionary_style(self):
        self.assertEqual(
            description_for(self.sign.term, self.org),
            "The process of entering account details to access a computer system or online service.",
        )
        self.assertNotIn("common service term", description_for("Assignment", self.org))

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

    def test_login_form_redirects_glossary_editor_to_editor_dashboard(self):
        response = self.client.post(
            reverse("login"),
            {"username": "glossary", "password": "pass12345"},
        )
        self.assertRedirects(response, reverse("dashboard_redirect"), fetch_redirect_response=False)
        response = self.client.get(response.url)
        self.assertRedirects(response, reverse("glossary_editor_dashboard", args=[self.org.slug]))

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
        self.assertNotContains(response, "Content queue")

    def test_glossary_editor_menu_contains_content_shortcuts(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("glossary_editor_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Glossary editor dashboard")
        self.assertContains(response, "Content queue")
        self.assertNotContains(response, "Assign tasks")

    def test_manager_organisation_home_does_not_duplicate_dashboard_actions(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertContains(response, "Manager dashboard")
        self.assertEqual(response.content.count(b">My dashboard</a>"), 1)

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
        self.assertContains(response, 'id="vue-staff-dashboard"')
        self.assertContains(response, 'data-dashboard-target="favourite-signs"')
        self.assertContains(response, 'class="dashboard-section dashboard-detail-fallback"')
        self.assertContains(response, "Your glossary activity")
        self.assertContains(response, reverse("staff_dashboard_api", args=[self.org.slug]))
        self.assertContains(response, "vue-staff-dashboard.js")

    def test_staff_dashboard_api_returns_staff_scoped_summary_for_vue(self):
        FavouriteSign.objects.create(staff_profile=self.profile, sign=self.sign)
        SignRequest.objects.create(
            organisation=self.org,
            requested_by=self.profile,
            term="Printer",
            context="Needed at the help desk.",
        )
        SignRequest.objects.create(
            organisation=self.other_org,
            term="Other request",
            requester_name="Visitor",
            requester_email="visitor@example.com",
            context="Other organisation.",
        )
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("staff_dashboard_api", args=[self.org.slug]))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["organisation"]["slug"], self.org.slug)
        self.assertEqual(payload["favourites"][0]["term"], "Login")
        self.assertEqual(payload["requests"][0]["term"], "Printer")
        self.assertNotIn("Other request", [item["term"] for item in payload["requests"]])

    def test_staff_dashboard_api_requires_login(self):
        response = self.client.get(reverse("staff_dashboard_api", args=[self.org.slug]))
        self.assertEqual(response.status_code, 302)

    def test_manager_dashboard_uses_organisation_theme(self):
        self.org.theme_colour = "#123abc"
        self.org.save()
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertContains(response, "--accent: #123abc")
        self.assertContains(response, "Welcome to College")
        self.assertContains(response, "Hi manager")

    def test_manager_dashboard_shows_review_workflow_counts(self):
        review_sign = SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Needs review",
            slug="needs-review",
            video_url="https://example.com/review",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Needs video",
            slug="needs-video",
            video_url="https://example.com/video",
            publication_status=SignEntry.PublicationStatus.NEEDS_VIDEO,
            video_review_status=SignEntry.VideoReviewStatus.NEEDS_REPLACEMENT,
        )
        SignEntry.objects.create(
            organisation=self.other_org,
            category=self.other_category,
            term="Other org draft",
            slug="other-org-draft",
            video_url="https://example.com/other-draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Pending requests")
        self.assertNotContains(response, "Signs needing review")
        self.assertNotContains(response, review_sign.term)
        self.assertNotContains(response, "Other org draft")

        self.client.logout()
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("glossary_editor_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Signs needing review")
        self.assertContains(response, "Signs needing video")
        self.assertContains(response, review_sign.term)
        self.assertNotContains(response, "Other org draft")

    def test_sign_and_request_pages_use_organisation_theme(self):
        self.org.theme_colour = "#123abc"
        self.org.save()
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertContains(response, "--accent: #123abc")
        response = self.client.get(reverse("request_sign", args=[self.org.slug]))
        self.assertContains(response, "--accent: #123abc")

    def test_sign_detail_renders_optional_transcript_and_thumbnail(self):
        self.sign.thumbnail_url = "https://example.com/login-thumb.jpg"
        self.sign.tags = "login, support, College"
        self.sign.save()
        Transcript.objects.create(sign=self.sign, text="Transcript text for the login sign.")
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertContains(response, "Transcript text for the login sign.")
        self.assertContains(response, 'src="https://example.com/login-thumb.jpg"')
        self.assertContains(response, 'alt="Thumbnail for Login ISL video"')
        self.assertContains(response, 'id="vue-sign-detail"')
        self.assertContains(response, 'id="sign-detail-data"')
        self.assertContains(response, "vue-sign-detail.js")
        self.assertContains(response, 'aria-label="Related glossary tags"')
        self.assertContains(response, reverse("category_detail", args=[self.org.slug, self.category.slug]))
        self.assertContains(response, f"{self.org.get_absolute_url()}?q=login")

    def test_unpublished_signs_are_hidden_from_public_and_staff_views(self):
        draft_sign = SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Draft only",
            slug="draft-only",
            video_url="https://example.com/draft",
            publication_status=SignEntry.PublicationStatus.DRAFT,
        )
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertNotContains(response, draft_sign.term)
        response = self.client.get(reverse("organisation_signs_api", args=[self.org.slug]))
        self.assertNotIn(draft_sign.term, [item["term"] for item in response.json()["results"]])
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, draft_sign.slug]))
        self.assertEqual(response.status_code, 404)

        self.client.login(username="staff", password="pass12345")
        FavouriteSign.objects.create(staff_profile=self.profile, sign=draft_sign)
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertNotContains(response, draft_sign.term)
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, draft_sign.slug]))
        self.assertEqual(response.status_code, 404)
        response = self.client.get(reverse("staff_dashboard", args=[self.org.slug]))
        self.assertNotContains(response, draft_sign.term)

    def test_manager_can_view_but_not_manage_own_organisation_review_needed_signs(self):
        draft_sign = SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Manager visible draft",
            slug="manager-visible-draft",
            video_url="https://example.com/draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        SignEntry.objects.create(
            organisation=self.other_org,
            category=self.other_category,
            term="Other manager draft",
            slug="other-manager-draft",
            video_url="https://example.com/other-draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertContains(response, draft_sign.term)
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, draft_sign.slug]))
        self.assertContains(response, draft_sign.term)
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertNotContains(response, draft_sign.term)
        self.assertNotContains(response, "Other manager draft")

    def test_glossary_editor_can_see_own_organisation_review_needed_signs_only(self):
        own_draft = SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Editor visible draft",
            slug="editor-visible-draft",
            video_url="https://example.com/draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        other_draft = SignEntry.objects.create(
            organisation=self.other_org,
            category=self.other_category,
            term="Other editor draft",
            slug="other-editor-draft",
            video_url="https://example.com/other-draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("organisation_home", args=[self.org.slug]))
        self.assertContains(response, own_draft.term)
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, own_draft.slug]))
        self.assertContains(response, own_draft.term)
        response = self.client.get(reverse("organisation_home", args=[self.other_org.slug]))
        self.assertNotContains(response, other_draft.term)
        response = self.client.get(reverse("sign_detail", args=[self.other_org.slug, other_draft.slug]))
        self.assertEqual(response.status_code, 404)

    def test_retail_dashboard_shows_retail_role_widgets(self):
        retail_user = User.objects.create_user(username="retail", password="pass12345")
        StaffProfile.objects.create(user=retail_user, organisation=self.other_org)
        self.client.login(username="retail", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[self.other_org.slug]))
        self.assertContains(response, "Clock-in reminder")
        self.assertContains(response, "floor tasks")

    def test_healthcare_dashboard_shows_appointment_role_widgets(self):
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

    def test_glossary_editor_is_redirected_from_staff_dashboard_to_editor_dashboard(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("staff_dashboard", args=[self.org.slug]))
        self.assertRedirects(response, reverse("glossary_editor_dashboard", args=[self.org.slug]))

    def test_glossary_editor_is_redirected_from_staff_task_board_to_editor_dashboard(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("task_board", args=[self.org.slug]))
        self.assertRedirects(response, reverse("glossary_editor_dashboard", args=[self.org.slug]))

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

    def test_staff_can_toggle_favourite_with_json_for_vue(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("toggle_favourite", args=[self.org.slug, self.sign.id]),
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_favourite"])
        self.assertTrue(FavouriteSign.objects.filter(staff_profile=self.profile, sign=self.sign).exists())

        response = self.client.post(
            reverse("toggle_favourite", args=[self.org.slug, self.sign.id]),
            HTTP_ACCEPT="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_favourite"])
        self.assertFalse(FavouriteSign.objects.filter(staff_profile=self.profile, sign=self.sign).exists())

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
                "request_type": SignRequest.RequestType.MISSING_SIGN,
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
        self.assertEqual(sign_request.request_type, SignRequest.RequestType.MISSING_SIGN)

    def test_staff_request_form_does_not_ask_for_contact_details(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("request_sign", args=[self.org.slug]))
        self.assertContains(response, "linked to your College staff profile")
        self.assertContains(response, 'id="vue-sign-request-form"')
        self.assertContains(response, "vue-request-form.js")
        self.assertContains(response, 'name="request_type"')
        self.assertNotContains(response, 'name="requester_name"')
        self.assertNotContains(response, 'name="requester_email"')

    def test_sign_detail_has_report_issue_link(self):
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertContains(response, "Report issue")
        self.assertContains(response, reverse("report_sign", args=[self.org.slug, self.sign.slug]))

    def test_staff_can_report_existing_sign_to_glossary_editor(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("report_sign", args=[self.org.slug, self.sign.slug]),
            {
                "request_type": SignRequest.RequestType.BROKEN_VIDEO_LINK,
                "context": "The video link does not load at the support desk.",
            },
        )
        self.assertRedirects(response, reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        sign_report = SignRequest.objects.get()
        self.assertEqual(sign_report.organisation, self.org)
        self.assertEqual(sign_report.related_sign, self.sign)
        self.assertEqual(sign_report.suggested_category, self.sign.category)
        self.assertEqual(sign_report.term, self.sign.term)
        self.assertEqual(sign_report.requested_by, self.profile)
        self.assertEqual(sign_report.request_type, SignRequest.RequestType.BROKEN_VIDEO_LINK)
        self.assertEqual(sign_report.status, SignRequest.Status.SENT_TO_INTERPRETER)

        self.client.logout()
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("glossary_editor_dashboard", args=[self.org.slug]))
        self.assertContains(response, "Broken video link")
        self.assertContains(response, "Reported sign")
        self.assertContains(response, self.sign.term)

    def test_existing_sign_report_does_not_enter_manager_triage_list(self):
        SignRequest.objects.create(
            organisation=self.org,
            requested_by=self.profile,
            related_sign=self.sign,
            suggested_category=self.sign.category,
            term=self.sign.term,
            request_type=SignRequest.RequestType.INCORRECT_SIGN,
            context="The sign seems incorrect.",
            status=SignRequest.Status.SENT_TO_INTERPRETER,
        )
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertNotContains(response, "The sign seems incorrect.")
        self.assertContains(response, "In glossary review")

    def test_visitor_can_report_existing_sign_with_contact_details(self):
        response = self.client.post(
            reverse("report_sign", args=[self.org.slug, self.sign.slug]),
            {
                "requester_name": "Visitor",
                "requester_email": "visitor@example.com",
                "request_type": SignRequest.RequestType.UNCLEAR_DESCRIPTION,
                "context": "The definition is not clear enough.",
            },
        )
        self.assertRedirects(response, reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        sign_report = SignRequest.objects.get()
        self.assertIsNone(sign_report.requested_by)
        self.assertEqual(sign_report.requester_email, "visitor@example.com")
        self.assertEqual(sign_report.related_sign, self.sign)
        self.assertEqual(sign_report.status, SignRequest.Status.SENT_TO_INTERPRETER)

    def test_visitor_can_submit_request_with_email(self):
        response = self.client.post(
            reverse("request_sign", args=[self.org.slug]),
            {
                "requester_name": "Visitor",
                "requester_email": "visitor@example.com",
                "request_type": SignRequest.RequestType.MISSING_SIGN,
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
        self.assertContains(response, 'id="vue-sign-request-form"')
        self.assertContains(response, "novalidate")
        self.assertContains(response, "vue-request-form.js")
        self.assertContains(response, 'name="requester_name"')
        self.assertContains(response, 'name="requester_email"')
        self.assertContains(response, 'name="request_type"')
        self.assertContains(response, 'id="requester-name-error"')
        self.assertContains(response, 'id="requester-email-error"')
        self.assertContains(response, 'id="term-error"')
        self.assertContains(response, 'id="context-error"')

    def test_manager_can_send_request_to_glossary_review(self):
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
                "admin_notes": "Suitable for glossary review.",
                "decision_reason": "The request is relevant to reception staff.",
            },
        )
        self.assertRedirects(response, reverse("manager_dashboard", args=[self.org.slug]))
        sign_request.refresh_from_db()
        self.assertEqual(sign_request.status, SignRequest.Status.MANAGER_APPROVED)
        self.assertEqual(sign_request.admin_notes, "Suitable for glossary review.")
        self.assertEqual(sign_request.decision_reason, "The request is relevant to reception staff.")
        self.assertEqual(sign_request.reviewed_by, self.manager_profile)
        self.assertIsNotNone(sign_request.reviewed_at)

    def test_manager_review_cannot_mark_request_as_completed(self):
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
                "admin_notes": "Trying to skip glossary review.",
            },
        )
        sign_request.refresh_from_db()
        self.assertEqual(sign_request.status, SignRequest.Status.PENDING)

    def test_staff_member_cannot_open_manager_dashboard(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertEqual(response.status_code, 404)

    def test_glossary_editor_cannot_open_manager_dashboard(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("manager_dashboard", args=[self.org.slug]))
        self.assertEqual(response.status_code, 404)

    def test_manager_cannot_open_glossary_editor_dashboard(self):
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("glossary_editor_dashboard", args=[self.org.slug]))
        self.assertEqual(response.status_code, 404)

    def test_staff_member_cannot_open_glossary_editor_dashboard(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("glossary_editor_dashboard", args=[self.org.slug]))
        self.assertEqual(response.status_code, 404)

    def test_glossary_editor_can_update_own_organisation_sign_workflow(self):
        draft_sign = SignEntry.objects.create(
            organisation=self.org,
            category=self.category,
            term="Draft sign",
            slug="draft-sign",
            video_url="https://example.com/draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
            video_review_status=SignEntry.VideoReviewStatus.CANDIDATE_VIDEO,
            is_official_published=False,
        )
        self.client.login(username="glossary", password="pass12345")
        response = self.client.post(
            reverse("update_sign_workflow", args=[self.org.slug, draft_sign.id]),
            {
                "publication_status": SignEntry.PublicationStatus.PUBLISHED,
                "video_review_status": SignEntry.VideoReviewStatus.APPROVED_FOR_PROTOTYPE,
            },
        )
        self.assertRedirects(response, reverse("glossary_editor_dashboard", args=[self.org.slug]))
        draft_sign.refresh_from_db()
        self.assertEqual(draft_sign.publication_status, SignEntry.PublicationStatus.PUBLISHED)
        self.assertEqual(
            draft_sign.video_review_status,
            SignEntry.VideoReviewStatus.APPROVED_FOR_PROTOTYPE,
        )
        self.assertTrue(draft_sign.is_official_published)

    def test_glossary_editor_cannot_update_other_organisation_sign_workflow(self):
        other_draft = SignEntry.objects.create(
            organisation=self.other_org,
            category=self.other_category,
            term="Other draft",
            slug="other-draft",
            video_url="https://example.com/other-draft",
            publication_status=SignEntry.PublicationStatus.NEEDS_REVIEW,
        )
        self.client.login(username="glossary", password="pass12345")
        response = self.client.post(
            reverse("update_sign_workflow", args=[self.other_org.slug, other_draft.id]),
            {
                "publication_status": SignEntry.PublicationStatus.PUBLISHED,
                "video_review_status": SignEntry.VideoReviewStatus.APPROVED_FOR_PROTOTYPE,
            },
        )
        self.assertEqual(response.status_code, 404)
        other_draft.refresh_from_db()
        self.assertEqual(other_draft.publication_status, SignEntry.PublicationStatus.NEEDS_REVIEW)

    def test_staff_member_cannot_update_sign_workflow(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.post(
            reverse("update_sign_workflow", args=[self.org.slug, self.sign.id]),
            {
                "publication_status": SignEntry.PublicationStatus.ARCHIVED,
                "video_review_status": SignEntry.VideoReviewStatus.BROKEN_LINK,
            },
        )
        self.assertEqual(response.status_code, 404)
        self.sign.refresh_from_db()
        self.assertEqual(self.sign.publication_status, SignEntry.PublicationStatus.PUBLISHED)

    def test_edit_sign_button_only_shows_for_glossary_editor(self):
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertNotContains(response, "Edit sign")

        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertNotContains(response, "Edit sign")

        self.client.logout()
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertNotContains(response, "Edit sign")

        self.client.logout()
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.assertContains(response, "Edit sign")
        self.assertContains(response, reverse("edit_sign", args=[self.org.slug, self.sign.slug]))

    def test_glossary_editor_can_edit_sign_from_app_and_log_changes(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.post(
            reverse("edit_sign", args=[self.org.slug, self.sign.slug]),
            {
                "category": self.category.id,
                "term": "Login",
                "slug": self.sign.slug,
                "description": "Updated definition for staff support.",
                "usage_context": "Used when helping users access college systems.",
                "tags": "login, account access, support",
                "video_url": "https://example.com/updated-login",
                "thumbnail_url": "",
                "publication_status": SignEntry.PublicationStatus.NEEDS_REVIEW,
                "video_review_status": SignEntry.VideoReviewStatus.NEEDS_REPLACEMENT,
                "is_quick_reference": "on",
            },
        )
        self.assertRedirects(response, reverse("sign_detail", args=[self.org.slug, self.sign.slug]))
        self.sign.refresh_from_db()
        self.assertEqual(self.sign.description, "Updated definition for staff support.")
        self.assertEqual(self.sign.tags, "login, account access, support")
        self.assertEqual(self.sign.publication_status, SignEntry.PublicationStatus.NEEDS_REVIEW)
        self.assertFalse(self.sign.is_official_published)

        log = SignEntryChangeLog.objects.get(sign=self.sign)
        self.assertEqual(log.edited_by, self.glossary_profile)
        self.assertIn("description", log.changed_fields)
        self.assertIn("tags", log.changed_fields)
        self.assertIn("Updated", log.change_summary)

    def test_staff_and_manager_cannot_open_sign_edit_page(self):
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("edit_sign", args=[self.org.slug, self.sign.slug]))
        self.assertEqual(response.status_code, 404)

        self.client.logout()
        self.client.login(username="manager", password="pass12345")
        response = self.client.get(reverse("edit_sign", args=[self.org.slug, self.sign.slug]))
        self.assertEqual(response.status_code, 404)

    def test_glossary_editor_cannot_edit_other_organisation_sign(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("edit_sign", args=[self.other_org.slug, self.other_sign.slug]))
        self.assertEqual(response.status_code, 404)

    def test_glossary_editor_cannot_access_django_admin(self):
        self.client.login(username="glossary", password="pass12345")
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

    def test_platform_admin_can_access_django_admin_without_groups(self):
        self.client.login(username="platform", password="pass12345")
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Groups")
        response = self.client.get(reverse("admin:glossary_organisation_changelist"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("admin:glossary_staffprofile_changelist"))
        self.assertEqual(response.status_code, 200)

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

    def test_model_validation_rejects_cross_organisation_related_sign_report(self):
        sign_request = SignRequest(
            organisation=self.org,
            requested_by=self.profile,
            related_sign=self.other_sign,
            term=self.other_sign.term,
            context="Wrong organisation report.",
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
