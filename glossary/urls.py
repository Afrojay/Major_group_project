from django.urls import path

from . import views

urlpatterns = [
    path("", views.organisation_list, name="organisation_list"),
    path("org/<slug:organisation_slug>/", views.organisation_home, name="organisation_home"),
    path(
        "org/<slug:organisation_slug>/category/<slug:category_slug>/",
        views.category_detail,
        name="category_detail",
    ),
    path(
        "org/<slug:organisation_slug>/sign/<slug:sign_slug>/",
        views.sign_detail,
        name="sign_detail",
    ),
    path(
        "org/<slug:organisation_slug>/dashboard/",
        views.staff_dashboard,
        name="staff_dashboard",
    ),
    path(
        "org/<slug:organisation_slug>/request/",
        views.request_sign,
        name="request_sign",
    ),
    path(
        "org/<slug:organisation_slug>/admin-dashboard/",
        views.organisation_admin_dashboard,
        name="organisation_admin_dashboard",
    ),
    path(
        "org/<slug:organisation_slug>/admin-dashboard/request/<int:request_id>/",
        views.review_sign_request,
        name="review_sign_request",
    ),
    path(
        "org/<slug:organisation_slug>/favourite/<int:sign_id>/",
        views.toggle_favourite,
        name="toggle_favourite",
    ),
]
