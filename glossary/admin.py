from django.contrib import admin

from .models import Category, FAQEntry, Organisation, SignEntry


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'contact_email', 'updated_at')
    search_fields = ('name', 'description', 'contact_email')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'slug', 'updated_at')
    list_filter = ('organisation',)
    search_fields = ('name', 'description', 'organisation__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SignEntry)
class SignEntryAdmin(admin.ModelAdmin):
    list_display = ('term', 'organisation', 'category', 'is_quick_reference', 'updated_at')
    list_filter = ('organisation', 'category', 'is_quick_reference')
    search_fields = ('term', 'description', 'usage_context', 'tags', 'organisation__name', 'category__name')
    prepopulated_fields = {'slug': ('term',)}


@admin.register(FAQEntry)
class FAQEntryAdmin(admin.ModelAdmin):
    list_display = ('question', 'organisation', 'related_category', 'related_sign', 'updated_at')
    list_filter = ('organisation', 'related_category')
    search_fields = ('question', 'answer', 'organisation__name')
