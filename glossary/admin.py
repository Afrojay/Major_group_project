from django.contrib import admin

from .models import (
    Category,
    FAQEntry,
    FavouriteSign,
    Organisation,
    PortalItem,
    SignEntry,
    SignRequest,
    StaffProfile,
    Transcript,
)


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

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "updated_at")
    list_filter = ("organisation",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "organisation__name")


@admin.register(SignEntry)
class SignEntryAdmin(admin.ModelAdmin):
    list_display = (
        "term",
        "organisation",
        "category",
        "is_quick_reference",
        "is_official_published",
        "updated_at",
    )
    list_filter = ("organisation", "category", "is_quick_reference", "is_official_published")
    prepopulated_fields = {"slug": ("term",)}
    search_fields = ("term", "description", "usage_context", "tags")

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(FAQEntry)
class FAQEntryAdmin(admin.ModelAdmin):
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


@admin.register(FavouriteSign)
class FavouriteSignAdmin(admin.ModelAdmin):
    list_display = ("staff_profile", "sign", "created_at")
    list_filter = ("staff_profile__organisation",)
    search_fields = ("staff_profile__user__username", "sign__term")

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(SignRequest)
class SignRequestAdmin(admin.ModelAdmin):
    list_display = ("term", "organisation", "requested_by", "requester_email", "status", "created_at")
    list_filter = ("organisation", "status", "suggested_category")
    search_fields = ("term", "context", "admin_notes", "requested_by__user__username")

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ("sign", "language", "updated_at")
    list_filter = ("language", "sign__organisation")
    search_fields = ("sign__term", "text")


@admin.register(PortalItem)
class PortalItemAdmin(admin.ModelAdmin):
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
