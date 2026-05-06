from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import SignRequestForm, SignRequestReviewForm
from .models import Category, FavouriteSign, Organisation, SignEntry, SignRequest


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


def _require_org_admin_profile(user, organisation):
    profile = _require_staff_profile(user, organisation)
    if not profile.is_organisation_admin:
        raise Http404("No organisation admin profile for this organisation.")
    return profile


def _search_signs(organisation, query):
    signs = organisation.signs.select_related("category")
    if not query:
        return signs
    return signs.filter(
        Q(term__icontains=query)
        | Q(description__icontains=query)
        | Q(usage_context__icontains=query)
        | Q(tags__icontains=query)
        | Q(category__name__icontains=query)
    )


def organisation_list(request):
    organisations = Organisation.objects.all()
    return render(
        request,
        "glossary/organisation_list.html",
        {"organisations": organisations},
    )


def organisation_home(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    query = request.GET.get("q", "").strip()
    signs = _search_signs(organisation, query)
    categories = organisation.categories.prefetch_related("signs")
    quick_signs = organisation.signs.filter(is_quick_reference=True).select_related("category")[:8]
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
            "signs": signs,
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
        SignEntry.objects.select_related("category", "organisation"),
        organisation=organisation,
        slug=sign_slug,
    )
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
            "staff_profile": profile,
            "is_favourite": is_favourite,
        },
    )


@login_required
def staff_dashboard(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_staff_profile(request.user, organisation)
    favourites = profile.favourites.select_related("sign", "sign__category")
    requests = profile.sign_requests.select_related("suggested_category")
    recent_signs = organisation.signs.select_related("category").order_by("-updated_at")[:5]
    quick_reference_count = organisation.signs.filter(is_quick_reference=True).count()
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
        },
    )


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
            sign_request.save()
            messages.success(request, "Your sign request has been submitted for admin review.")
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
def organisation_admin_dashboard(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    profile = _require_org_admin_profile(request.user, organisation)
    requests = organisation.sign_requests.select_related(
        "requested_by",
        "requested_by__user",
        "suggested_category",
    )
    status_counts = {
        item["status"]: item["total"]
        for item in organisation.sign_requests.values("status").annotate(total=Count("id"))
    }
    return render(
        request,
        "glossary/organisation_admin_dashboard.html",
        {
            "organisation": organisation,
            "staff_profile": profile,
            "requests": requests,
            "pending_count": status_counts.get(SignRequest.Status.PENDING, 0),
            "approved_count": status_counts.get(SignRequest.Status.APPROVED, 0),
            "needs_clarification_count": status_counts.get(
                SignRequest.Status.NEEDS_CLARIFICATION,
                0,
            ),
            "rejected_count": status_counts.get(SignRequest.Status.REJECTED, 0),
            "sign_count": organisation.signs.count(),
            "category_count": organisation.categories.count(),
            "staff_count": organisation.staff_profiles.count(),
        },
    )


@login_required
@require_POST
def review_sign_request(request, organisation_slug, request_id):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    _require_org_admin_profile(request.user, organisation)
    sign_request = get_object_or_404(SignRequest, id=request_id, organisation=organisation)
    form = SignRequestReviewForm(request.POST, instance=sign_request)
    if form.is_valid():
        form.save()
        messages.success(request, f"{sign_request.term} request was updated.")
    else:
        messages.error(request, "The request could not be updated.")
    return redirect("organisation_admin_dashboard", organisation_slug=organisation.slug)
