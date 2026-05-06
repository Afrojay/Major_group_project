from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import AssignedTaskForm, PortalItemForm, SignRequestForm, SignRequestReviewForm
from .models import Category, FavouriteSign, Organisation, PortalItem, SignEntry, SignRequest

ALPHABET = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


class StaffLoginView(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        user = form.get_user()
        profile = getattr(user, "staff_profile", None)
        if profile:
            messages.success(
                self.request,
                f"Welcome back, {user.get_full_name() or user.get_username()} - {profile.organisation.name}.",
            )
        else:
            messages.info(self.request, "Welcome back. No staff profile is linked to this account yet.")
        return super().form_valid(form)


def _staff_profile_for(user, organisation):
    if not user.is_authenticated:
        return None
    profile = getattr(user, "staff_profile", None)
    if profile and profile.organisation_id == organisation.id:
        return profile
    return None


def _require_staff_profile(user, organisation):
    profile = _staff_profile_for(user, organisation)
    if profile is None:
        raise Http404("No staff profile for this organisation.")
    return profile


def _require_request_reviewer_profile(user, organisation):
    profile = _require_staff_profile(user, organisation)
    if not profile.can_review_requests:
        raise Http404("No manager profile for this organisation.")
    return profile


def _search_signs(organisation, query, category_slug="", letter=""):
    signs = organisation.signs.select_related("category")
    if category_slug:
        signs = signs.filter(category__slug=category_slug)
    if letter:
        signs = signs.filter(term__istartswith=letter)
    if not query:
        return signs
    return signs.filter(
        Q(term__icontains=query)
        | Q(description__icontains=query)
        | Q(usage_context__icontains=query)
        | Q(tags__icontains=query)
        | Q(category__name__icontains=query)
    )


def _portal_cards_for(organisation, profile):
    slug = organisation.slug
    cards = [
        {
            "title": "My quick links",
            "body": "Open the organisation glossary, saved signs, and request forms from one place.",
            "status": "Staff tools",
            "href": organisation.get_absolute_url(),
            "link_label": "Open glossary",
        }
    ]
    if "retail" in slug:
        cards.extend(
            [
                {
                    "title": "Clock-in reminder",
                    "body": "Shift clock-in, break tracking, and handover reminders for the retail workspace.",
                    "status": "Retail workflow",
                },
                {
                    "title": "Today's floor tasks",
                    "body": "Check tills, queue support, refunds, and customer service priorities.",
                    "status": "Retail workflow",
                    "href": organisation.get_absolute_url(),
                    "link_label": "Open customer service signs",
                },
            ]
        )
    elif "college" in slug:
        cards.extend(
            [
                {
                    "title": "Department calendar",
                    "body": "Labs, office hours, assessment windows, and support sessions for staff awareness.",
                    "status": "College workflow",
                },
                {
                    "title": "Student support queue",
                    "body": "Track common support terms such as login, password, assignments, and databases.",
                    "status": "Support workflow",
                    "href": organisation.get_absolute_url(),
                    "link_label": "Open student support signs",
                },
            ]
        )
    elif "healthcare" in slug:
        cards.extend(
            [
                {
                    "title": "Upcoming appointments",
                    "body": "09:30 - New patient check-in; 10:15 - Interpreter requested; 11:00 - Follow-up arrival.",
                    "status": "Reception workflow",
                    "action_label": "+ Add appointment",
                },
                {
                    "title": "Accessibility needs",
                    "body": "Track non-clinical access notes such as interpreter needed, quiet waiting area, or written instructions.",
                    "status": "Access notes",
                    "action_label": "+ Add note",
                    "href": organisation.get_absolute_url(),
                    "link_label": "Open access signs",
                },
            ]
        )
    else:
        cards.extend(
            [
                {
                    "title": "Team notices",
                    "body": "Organisation-specific staff notices and accessibility reminders.",
                    "status": "Team workflow",
                },
                {
                    "title": "Today's actions",
                    "body": "Daily tasks configured for the organisation.",
                    "status": "Team workflow",
                },
            ]
        )

    if profile.can_review_requests:
        cards.append(
            {
                "title": "Manager to-dos",
                "body": "Review pending sign requests and decide whether they need clarification or interpreter review.",
                "status": "Reviewer access",
                "href": reverse("manager_dashboard", kwargs={"organisation_slug": organisation.slug}),
                "link_label": "Review requests",
            }
        )
    if profile.can_prepare_glossary_content:
        cards.append(
            {
                "title": "Glossary preparation",
                "body": "Prepare manager-approved requests for interpreter/content review in the back office.",
                "status": "Glossary manager",
                "href": reverse("manager_dashboard", kwargs={"organisation_slug": organisation.slug}),
                "link_label": "Open review pipeline",
            }
        )
    return cards


def _default_portal_item_type(organisation):
    slug = organisation.slug
    if "healthcare" in slug:
        return PortalItem.ItemType.APPOINTMENT
    if "college" in slug:
        return PortalItem.ItemType.CALENDAR_EVENT
    if "retail" in slug:
        return PortalItem.ItemType.TASK
    return PortalItem.ItemType.NOTE


def _portal_item_heading(organisation):
    item_type = _default_portal_item_type(organisation)
    return {
        PortalItem.ItemType.APPOINTMENT: "Appointments and access notes",
        PortalItem.ItemType.CALENDAR_EVENT: "Calendar and support items",
        PortalItem.ItemType.TASK: "Tasks and shift items",
        PortalItem.ItemType.NOTE: "Team notes",
    }.get(item_type, "Team notes")


def _user_display_name(user):
    return user.get_full_name() or user.get_username()


def _portal_hero_context(user, profile, organisation, portal_type):
    if portal_type == "manager":
        return {
            "eyebrow": f"{profile.get_role_type_display()} workspace",
            "title": f"Welcome to {organisation.name}",
            "message": (
                f"Hi {_user_display_name(user)}. You can triage sign requests, "
                "assign staff tasks, and prepare approved items for interpreter/content review."
            ),
            "actions": [
                {"label": "View public glossary", "href": organisation.get_absolute_url(), "class": "button"},
            ],
            "show_time": False,
        }
    return {
        "eyebrow": f"{profile.get_role_type_display()} portal",
        "title": f"Welcome to {organisation.name}",
        "message": (
            f"Hi {_user_display_name(user)}. Favourites, assigned tasks, and sign requests "
            "are scoped to your staff profile for this organisation."
        ),
        "actions": [
            {
                "label": "Request a missing sign",
                "href": reverse("request_sign", kwargs={"organisation_slug": organisation.slug}),
                "class": "button",
            },
            {"label": "Browse glossary", "href": organisation.get_absolute_url(), "class": "button secondary"},
            {
                "label": "Tasks",
                "href": reverse("task_board", kwargs={"organisation_slug": organisation.slug}),
                "class": "button secondary",
            },
        ],
        "show_time": True,
    }


def organisation_list(request):
    organisations = Organisation.objects.all()
    return render(
        request,
        "glossary/organisation_list.html",
        {"organisations": organisations},
    )


@login_required
def dashboard_redirect(request):
    profile = getattr(request.user, "staff_profile", None)
    if profile:
        if profile.can_review_requests:
            return redirect("manager_dashboard", organisation_slug=profile.organisation.slug)
        return redirect("staff_dashboard", organisation_slug=profile.organisation.slug)
    messages.info(request, "No staff profile is linked to this account yet.")
    return redirect("organisation_list")


def organisation_home(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    query = request.GET.get("q", "").strip()
    selected_category_slug = request.GET.get("category", "").strip()
    selected_letter = request.GET.get("letter", "").strip().upper()[:1]
    if selected_letter not in ALPHABET:
        selected_letter = ""
    selected_category = None
    if selected_category_slug:
        selected_category = get_object_or_404(
            Category,
            organisation=organisation,
            slug=selected_category_slug,
        )
    signs = _search_signs(organisation, query, selected_category_slug, selected_letter)
    categories = organisation.categories.annotate(sign_count=Count("signs")).prefetch_related("signs")
    quick_signs = organisation.signs.filter(is_quick_reference=True).select_related("category")
    if selected_category:
        quick_signs = quick_signs.filter(category=selected_category)
    quick_signs = quick_signs[:8]
    faqs = organisation.faqs.select_related("related_category", "related_sign")[:6]
    favourite_ids = set()
    profile = _staff_profile_for(request.user, organisation)
    if profile:
        favourite_ids = set(profile.favourites.values_list("sign_id", flat=True))
    return render(
        request,
        "glossary/organisation_home.html",
        {
            "organisation": organisation,
            "categories": categories,
            "query": query,
            "alphabet": ALPHABET,
            "selected_category": selected_category,
            "selected_category_slug": selected_category_slug,
            "selected_letter": selected_letter,
            "signs": signs,
            "result_count": signs.count(),
            "total_sign_count": organisation.signs.count(),
            "quick_signs": quick_signs,
            "faqs": faqs,
            "staff_profile": profile,
            "favourite_ids": favourite_ids,
        },
    )


def category_detail(request, organisation_slug, category_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    category = get_object_or_404(
        Category,
        organisation=organisation,
        slug=category_slug,
    )
    signs = category.signs.select_related("organisation", "category")
    return render(
        request,
        "glossary/category_detail.html",
        {
            "organisation": organisation,
            "category": category,
            "signs": signs,
        },
    )


def sign_detail(request, organisation_slug, sign_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    sign = get_object_or_404(
        SignEntry.objects.select_related("category", "organisation", "transcript"),
        organisation=organisation,
        slug=sign_slug,
    )
    try:
        transcript = sign.transcript
    except ObjectDoesNotExist:
        transcript = None
    profile = _staff_profile_for(request.user, organisation)
    is_favourite = False
    if profile:
        is_favourite = FavouriteSign.objects.filter(staff_profile=profile, sign=sign).exists()
    return render(
        request,
        "glossary/sign_detail.html",
        {
            "organisation": organisation,
            "sign": sign,
            "transcript": transcript,
            "staff_profile": profile,
            "is_favourite": is_favourite,
        },
    )


@login_required
def staff_dashboard(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_staff_profile(request.user, organisation)
    if profile.can_review_requests:
        return redirect("manager_dashboard", organisation_slug=organisation.slug)
    favourites = profile.favourites.select_related("sign", "sign__category")
    requests = profile.sign_requests.select_related("suggested_category")
    recent_signs = organisation.signs.select_related("category").order_by("-updated_at")[:5]
    quick_reference_count = organisation.signs.filter(is_quick_reference=True).count()
    pending_review_count = 0
    if profile.can_review_requests:
        pending_review_count = organisation.sign_requests.filter(status=SignRequest.Status.PENDING).count()
    default_item_type = _default_portal_item_type(organisation)
    portal_items = organisation.portal_items.filter(item_type=default_item_type)[:8]
    assigned_task_count = organisation.portal_items.filter(
        assigned_to=profile,
        is_complete=False,
    ).count()
    return render(
        request,
        "glossary/staff_dashboard.html",
        {
            "organisation": organisation,
            "staff_profile": profile,
            "favourites": favourites,
            "requests": requests,
            "recent_signs": recent_signs,
            "quick_reference_count": quick_reference_count,
            "pending_review_count": pending_review_count,
            "assigned_task_count": assigned_task_count,
            "portal_cards": _portal_cards_for(organisation, profile),
            "portal_items": portal_items,
            "portal_item_form": PortalItemForm(default_item_type=default_item_type),
            "portal_item_heading": _portal_item_heading(organisation),
            "portal_hero": _portal_hero_context(request.user, profile, organisation, "staff"),
            "current_time": timezone.localtime(),
        },
    )


@login_required
@require_POST
def create_portal_item(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_staff_profile(request.user, organisation)
    default_item_type = _default_portal_item_type(organisation)
    form = PortalItemForm(request.POST, default_item_type=default_item_type)
    if form.is_valid():
        item = form.save(commit=False)
        item.organisation = organisation
        item.created_by = profile
        item.item_type = default_item_type
        item.full_clean()
        item.save()
        messages.success(request, f"{item.title} was added to the dashboard.")
    else:
        messages.error(request, "The dashboard item could not be added.")
    return redirect("staff_dashboard", organisation_slug=organisation.slug)


@login_required
def task_board(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_staff_profile(request.user, organisation)
    if profile.can_review_requests:
        return redirect("manager_dashboard", organisation_slug=organisation.slug)
    tasks = organisation.portal_items.filter(
        item_type=PortalItem.ItemType.TASK,
        assigned_to=profile,
    ).select_related("assigned_to", "assigned_to__user", "created_by", "created_by__user")
    return render(
        request,
        "glossary/task_board.html",
        {
            "organisation": organisation,
            "staff_profile": profile,
            "tasks": tasks,
            "task_form": AssignedTaskForm(organisation=organisation),
        },
    )


@login_required
@require_POST
def create_assigned_task(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_request_reviewer_profile(request.user, organisation)
    form = AssignedTaskForm(request.POST, organisation=organisation)
    if form.is_valid():
        task = form.save(commit=False)
        task.organisation = organisation
        task.created_by = profile
        task.item_type = PortalItem.ItemType.TASK
        task.full_clean()
        task.save()
        messages.success(request, f"{task.title} was assigned.")
    else:
        messages.error(request, "The task could not be assigned.")
    return redirect("manager_dashboard", organisation_slug=organisation.slug)


@login_required
@require_POST
def complete_portal_item(request, organisation_slug, item_id):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_staff_profile(request.user, organisation)
    item = get_object_or_404(PortalItem, id=item_id, organisation=organisation)
    if item.assigned_to_id and item.assigned_to_id != profile.id and not profile.can_review_requests:
        raise Http404("This task is not assigned to this staff profile.")
    item.is_complete = True
    item.save(update_fields=["is_complete", "updated_at"])
    messages.success(request, f"{item.title} was marked complete.")
    next_url = request.POST.get("next")
    if next_url and next_url.startswith("/"):
        return redirect(next_url)
    return redirect("staff_dashboard", organisation_slug=organisation.slug)


def request_sign(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _staff_profile_for(request.user, organisation)
    if request.method == "POST":
        form = SignRequestForm(request.POST, organisation=organisation, staff_profile=profile)
        if form.is_valid():
            sign_request = form.save(commit=False)
            sign_request.organisation = organisation
            sign_request.requested_by = profile
            if profile:
                sign_request.requester_name = request.user.get_full_name() or request.user.get_username()
                sign_request.requester_email = request.user.email
            sign_request.full_clean()
            sign_request.save()
            messages.success(request, "Your sign request has been submitted for manager review.")
            if profile:
                return redirect("staff_dashboard", organisation_slug=organisation.slug)
            return redirect("organisation_home", organisation_slug=organisation.slug)
    else:
        form = SignRequestForm(organisation=organisation, staff_profile=profile)
    return render(
        request,
        "glossary/request_sign.html",
        {
            "organisation": organisation,
            "form": form,
            "staff_profile": profile,
        },
    )


@login_required
@require_POST
def toggle_favourite(request, organisation_slug, sign_id):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_staff_profile(request.user, organisation)
    sign = get_object_or_404(SignEntry, id=sign_id, organisation=organisation)
    favourite, created = FavouriteSign.objects.get_or_create(staff_profile=profile, sign=sign)
    if created:
        messages.success(request, f"{sign.term} was added to your favourites.")
    else:
        favourite.delete()
        messages.info(request, f"{sign.term} was removed from your favourites.")
    return redirect(request.POST.get("next") or sign.get_absolute_url())


@login_required
def manager_dashboard(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_request_reviewer_profile(request.user, organisation)
    requests = organisation.sign_requests.select_related(
        "requested_by",
        "requested_by__user",
        "suggested_category",
    )
    status_counts = {
        item["status"]: item["total"]
        for item in organisation.sign_requests.values("status").annotate(total=Count("id"))
    }
    tasks = organisation.portal_items.filter(item_type=PortalItem.ItemType.TASK).select_related(
        "assigned_to",
        "assigned_to__user",
        "created_by",
        "created_by__user",
    )
    return render(
        request,
        "glossary/manager_dashboard.html",
        {
            "organisation": organisation,
            "staff_profile": profile,
            "requests": requests,
            "pending_count": status_counts.get(SignRequest.Status.PENDING, 0),
            "manager_approved_count": status_counts.get(SignRequest.Status.MANAGER_APPROVED, 0),
            "sent_to_interpreter_count": status_counts.get(SignRequest.Status.SENT_TO_INTERPRETER, 0),
            "completed_count": status_counts.get(SignRequest.Status.COMPLETED, 0),
            "needs_clarification_count": status_counts.get(
                SignRequest.Status.NEEDS_CLARIFICATION,
                0,
            ),
            "rejected_count": status_counts.get(SignRequest.Status.REJECTED, 0),
            "sign_count": organisation.signs.count(),
            "category_count": organisation.categories.count(),
            "staff_count": organisation.staff_profiles.count(),
            "tasks": tasks,
            "task_form": AssignedTaskForm(organisation=organisation),
            "portal_hero": _portal_hero_context(request.user, profile, organisation, "manager"),
        },
    )


@login_required
@require_POST
def review_sign_request(request, organisation_slug, request_id):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    _require_request_reviewer_profile(request.user, organisation)
    sign_request = get_object_or_404(SignRequest, id=request_id, organisation=organisation)
    form = SignRequestReviewForm(request.POST, instance=sign_request)
    if form.is_valid():
        form.save()
        messages.success(request, f"{sign_request.term} request was updated.")
    else:
        messages.error(request, "The request could not be updated.")
    return redirect("manager_dashboard", organisation_slug=organisation.slug)
