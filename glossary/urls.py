from django.urls import path

from . import views

urlpatterns = [
    path("", views.organisation_list, name="organisation_list"),
    path("dashboard/", views.dashboard_redirect, name="dashboard_redirect"),
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
        "org/<slug:organisation_slug>/dashboard/items/",
        views.create_portal_item,
        name="create_portal_item",
    ),
    path(
        "org/<slug:organisation_slug>/dashboard/items/<int:item_id>/complete/",
        views.complete_portal_item,
        name="complete_portal_item",
    ),
    path(
        "org/<slug:organisation_slug>/tasks/",
        views.task_board,
        name="task_board",
    ),
    path(
        "org/<slug:organisation_slug>/tasks/create/",
        views.create_assigned_task,
        name="create_assigned_task",
    ),
    path(
        "org/<slug:organisation_slug>/request/",
        views.request_sign,
        name="request_sign",
    ),
    path(
        "org/<slug:organisation_slug>/manager-dashboard/",
        views.manager_dashboard,
        name="manager_dashboard",
    ),
    path(
        "org/<slug:organisation_slug>/manager-dashboard/request/<int:request_id>/",
        views.review_sign_request,
        name="review_sign_request",
    ),
    path(
        "org/<slug:organisation_slug>/favourite/<int:sign_id>/",
        views.toggle_favourite,
        name="toggle_favourite",
    ),
]
