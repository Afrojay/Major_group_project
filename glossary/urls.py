from django.urls import path

from . import views

app_name = 'glossary'

urlpatterns = [
    path('', views.home, name='home'),
    path('org/<slug:organisation_slug>/', views.organisation_home, name='organisation_home'),
    path('org/<slug:organisation_slug>/category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('org/<slug:organisation_slug>/sign/<slug:sign_slug>/', views.sign_detail, name='sign_detail'),
    path('org/<slug:organisation_slug>/search/', views.search_results, name='search_results'),
    path('org/<slug:organisation_slug>/quick-reference/', views.quick_reference, name='quick_reference'),
]
