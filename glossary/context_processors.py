def staff_portal(request):
    if not request.user.is_authenticated:
        return {
            "current_staff_profile": None,
            "current_staff_organisation": None,
        }
    profile = getattr(request.user, "staff_profile", None)
    return {
        "current_staff_profile": profile,
        "current_staff_organisation": profile.organisation if profile else None,
    }
