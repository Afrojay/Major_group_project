from django.contrib import admin

from .models import (
    Category,
    FAQEntry,
    FavouriteSign,
    Organisation,
    SignEntry,
    SignRequest,
    StaffProfile,
)


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "contact_email", "updated_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "updated_at")
    list_filter = ("organisation",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description", "organisation__name")


@admin.register(SignEntry)
class SignEntryAdmin(admin.ModelAdmin):
    list_display = ("term", "organisation", "category", "is_quick_reference", "updated_at")
    list_filter = ("organisation", "category", "is_quick_reference")
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
    list_display = ("user", "organisation", "role", "is_organisation_admin", "updated_at")
    list_filter = ("organisation", "is_organisation_admin")
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
