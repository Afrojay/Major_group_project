from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    Category,
    FAQEntry,
    FavouriteSign,
    Organisation,
    PortalItem,
    SignEntry,
    SignEntryChangeLog,
    SignRequest,
    StaffProfile,
    Transcript,
)


admin.site.unregister(Group)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("name", "slug", "description")}),
        (
            "Organisation branding",
            {"fields": ("theme_colour", "logo_url", "contact_email")},
        ),
    )
    list_display = ("name", "slug", "theme_colour", "contact_email", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "contact_email")

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


class OrganisationScopedAdminMixin:
    organisation_lookup = "organisation"

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def _staff_profile(self, request):
        return getattr(request.user, "staff_profile", None)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        profile = self._staff_profile(request)
        if not profile:
            return queryset.none()
        return queryset.filter(**{self.organisation_lookup: profile.organisation})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        profile = self._staff_profile(request)
        if profile and not request.user.is_superuser:
            if db_field.name == "organisation":
                kwargs["queryset"] = Organisation.objects.filter(id=profile.organisation_id)
            elif db_field.name in {"category", "suggested_category", "related_category"}:
                kwargs["queryset"] = Category.objects.filter(organisation=profile.organisation)
            elif db_field.name in {"sign", "related_sign"}:
                kwargs["queryset"] = SignEntry.objects.filter(organisation=profile.organisation)
            elif db_field.name in {"requested_by", "reviewed_by", "created_by", "assigned_to"}:
                kwargs["queryset"] = StaffProfile.objects.filter(organisation=profile.organisation)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    list_display = ("name", "organisation", "updated_at")
    list_filter = ("organisation",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "organisation__name")


@admin.register(SignEntry)
class SignEntryAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    list_display = (
        "term",
        "organisation",
        "category",
        "publication_status",
        "video_review_status",
        "is_quick_reference",
        "is_official_published",
        "updated_at",
    )
    list_filter = (
        "organisation",
        "category",
        "publication_status",
        "video_review_status",
        "is_quick_reference",
        "is_official_published",
    )
    prepopulated_fields = {"slug": ("term",)}
    search_fields = ("term", "description", "usage_context", "tags")
    fieldsets = (
        (None, {"fields": ("organisation", "category", "term", "slug")}),
        ("Glossary content", {"fields": ("description", "usage_context", "tags")}),
        ("Video", {"fields": ("video_url", "thumbnail_url", "video_review_status")}),
        (
            "Publication workflow",
            {
                "fields": (
                    "publication_status",
                    "is_official_published",
                    "is_quick_reference",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(SignEntryChangeLog)
class SignEntryChangeLogAdmin(admin.ModelAdmin):
    list_display = ("sign", "edited_by", "changed_fields", "created_at")
    list_filter = ("sign__organisation", "edited_by", "created_at")
    search_fields = ("sign__term", "changed_fields", "change_summary", "edited_by__user__username")
    readonly_fields = ("sign", "edited_by", "changed_fields", "change_summary", "created_at", "updated_at")

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(FAQEntry)
class FAQEntryAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    list_display = ("question", "organisation", "related_category", "updated_at")
    list_filter = ("organisation", "related_category")
    search_fields = ("question", "answer")

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "role_type", "updated_at")
    list_filter = ("organisation", "role_type")
    search_fields = ("user__username", "user__email", "role", "organisation__name")

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(FavouriteSign)
class FavouriteSignAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    organisation_lookup = "staff_profile__organisation"
    list_display = ("staff_profile", "sign", "created_at")
    list_filter = ("staff_profile__organisation",)
    search_fields = ("staff_profile__user__username", "sign__term")

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(SignRequest)
class SignRequestAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    list_display = (
        "term",
        "request_type",
        "organisation",
        "related_sign",
        "requested_by",
        "requester_email",
        "status",
        "reviewed_by",
        "reviewed_at",
        "created_at",
    )
    list_filter = (
        "organisation",
        "request_type",
        "status",
        "suggested_category",
        "related_sign",
        "reviewed_by",
    )
    search_fields = (
        "term",
        "context",
        "admin_notes",
        "decision_reason",
        "requested_by__user__username",
        "reviewed_by__user__username",
        "related_sign__term",
    )
    readonly_fields = ("reviewed_at",)
    fieldsets = (
        (
            "Request",
            {
                "fields": (
                    "organisation",
                    "request_type",
                    "term",
                    "context",
                    "suggested_category",
                    "related_sign",
                )
            },
        ),
        (
            "Requester",
            {"fields": ("requested_by", "requester_name", "requester_email")},
        ),
        (
            "Review workflow",
            {
                "fields": (
                    "status",
                    "admin_notes",
                    "decision_reason",
                    "approval_notes",
                    "interpreter_notes",
                    "reviewed_by",
                    "reviewed_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Transcript)
class TranscriptAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    organisation_lookup = "sign__organisation"
    list_display = ("sign", "language", "updated_at")
    list_filter = ("language", "sign__organisation")
    search_fields = ("sign__term", "text")


@admin.register(PortalItem)
class PortalItemAdmin(OrganisationScopedAdminMixin, admin.ModelAdmin):
    list_display = ("title", "organisation", "item_type", "assigned_to", "due_at", "is_complete", "updated_at")
    list_filter = ("organisation", "item_type", "is_complete", "assigned_to")
    search_fields = (
        "title",
        "description",
        "organisation__name",
        "created_by__user__username",
        "assigned_to__user__username",
    )

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
