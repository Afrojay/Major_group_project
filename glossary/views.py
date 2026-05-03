from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .forms import SignSearchForm
from .models import Category, Organisation, SignEntry


def home(request):
    organisations = Organisation.objects.all()
    return render(request, 'glossary/home.html', {'organisations': organisations})


def organisation_home(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    categories = organisation.categories.all()
    quick_signs = organisation.signs.filter(is_quick_reference=True)[:6]
    search_form = SignSearchForm()
    return render(request, 'glossary/organisation_home.html', {
        'organisation': organisation,
        'categories': categories,
        'quick_signs': quick_signs,
        'search_form': search_form,
    })


def category_detail(request, organisation_slug, category_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    category = get_object_or_404(Category, organisation=organisation, slug=category_slug)
    signs = category.signs.all()
    return render(request, 'glossary/category_detail.html', {
        'organisation': organisation,
        'category': category,
        'signs': signs,
    })


def sign_detail(request, organisation_slug, sign_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    sign = get_object_or_404(SignEntry, organisation=organisation, slug=sign_slug)
    related_signs = SignEntry.objects.filter(
        organisation=organisation,
        category=sign.category,
    ).exclude(pk=sign.pk)[:4]
    return render(request, 'glossary/sign_detail.html', {
        'organisation': organisation,
        'sign': sign,
        'related_signs': related_signs,
    })


def search_results(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    form = SignSearchForm(request.GET)
    query = ''
    results = SignEntry.objects.filter(organisation=organisation)

    if form.is_valid():
        query = form.cleaned_data.get('q', '').strip()
        if query:
            results = results.filter(
                Q(term__icontains=query)
                | Q(description__icontains=query)
                | Q(usage_context__icontains=query)
                | Q(tags__icontains=query)
                | Q(category__name__icontains=query)
            )

    return render(request, 'glossary/search_results.html', {
        'organisation': organisation,
        'form': form,
        'query': query,
        'results': results,
    })


def quick_reference(request, organisation_slug):
    organisation = get_object_or_404(Organisation, slug=organisation_slug)
    signs = organisation.signs.filter(is_quick_reference=True)
    return render(request, 'glossary/quick_reference.html', {
        'organisation': organisation,
        'signs': signs,
    })
